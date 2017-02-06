import fileinput 
from pox.core import core
from pox.lib.addresses import IPAddr,EthAddr,parse_cidr
from pox.lib.revent import EventContinue,EventHalt
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

import sys

log = core.getLogger()
#log = core.getLogger()

serverList = {}
server_virtual_ip = ""
server_virtual_mac= ""
def launch (virtual_ip = "10.0.0.5", virtual_mac = "00:00:00:00:00:05",server_config="config.txt"):
    global serverList
    global server_virtual_ip
    global server_virtual_mac
    # To intercept packets before the learning switch
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn, priority=2)
    log.info("Stateless LB running.")
    file_name = server_config
    f = open(file_name)
    data = f.readlines()
    #print (data)
    f.close()
    i=0
    for line in data:
        columns=line.split()
        if (columns.__len__()==0):
	        break
        serverList[i]={'ip':IPAddr(columns[0]), 'mac':EthAddr(columns[1]), 'port': int(columns[2])}
        #serverList[i]={'ip':columns[0], 'mac':columns[1], 'outport': columns[2]}
        print (serverList[i]['ip'])
        i=i+1
	print (i)

    server_virtual_ip = IPAddr(virtual_ip)
    server_virtual_mac = EthAddr(virtual_mac)
    print (server_virtual_ip)
    print (server_virtual_mac)
	
#Round Robin

ServerUsed = 0 

def _handle_PacketIn (event):
    global ServerUsed
    global serverList
    global server_virtual_ip
    global server_virtual_mac
    packet = event.parsed
    # Only handle IPv4 flows

    if (not event.parsed.find("ipv4")):
        return EventContinue

    msg_to_server = of.ofp_flow_mod()
    msg_to_server.match = of.ofp_match.from_packet(packet)

    # Only handle traffic destined to virtual IP

    if (msg_to_server.match.nw_dst != server_virtual_ip):
        return EventContinue
    print ('Server in Service => Server :', ServerUsed)
    server_ip =  serverList[ServerUsed] ['ip'] 
    print serverList[ServerUsed] ['ip'] 
    print ('With IP => ServerIP = :', server_ip)   
    server_mac= serverList[ServerUsed]['mac']  
    server_outport= serverList[ServerUsed]['port']
    ServerUsed = (ServerUsed + 1)% serverList.__len__()
    print serverList.__len__()

    # Setup route to server

    msg_to_server.buffer_id = event.ofp.buffer_id
    msg_to_server.in_port = event.port
    msg_to_server.actions.append(of.ofp_action_dl_addr(of.OFPAT_SET_DL_DST, server_mac))
    msg_to_server.actions.append(of.ofp_action_nw_addr(of.OFPAT_SET_NW_DST, server_ip))
    msg_to_server.actions.append(of.ofp_action_output(port = server_outport))

    event.connection.send(msg_to_server)

    # Setup reverse route from server

    msg_from_server = of.ofp_flow_mod()
    msg_from_server.buffer_id = None
    msg_from_server.in_port = server_outport

    msg_from_server.match = of.ofp_match()
    msg_from_server.match.dl_src = server_mac
    msg_from_server.match.nw_src = server_ip
    msg_from_server.match.tp_src = msg_to_server.match.tp_dst

    msg_from_server.match.dl_dst = msg_to_server.match.dl_src
    msg_from_server.match.nw_dst = msg_to_server.match.nw_src
    msg_from_server.match.tp_dst = msg_to_server.match.tp_src

    msg_from_server.actions.append(of.ofp_action_dl_addr(of.OFPAT_SET_DL_SRC, server_virtual_mac))
    msg_from_server.actions.append(of.ofp_action_nw_addr(of.OFPAT_SET_NW_SRC, server_virtual_ip))
    msg_from_server.actions.append(of.ofp_action_output(port = msg_to_server.in_port))

    event.connection.send(msg_from_server)

    return EventHalt


