from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
 
import csv
 
log = core.getLogger()
denyList=[] 

class Firewall (EventMixin):
 
    def __init__ (self):
	self.listenTo(core.openflow)
        log.debug("Firewall Enabled")
        
    def _handle_ConnectionUp (self, event): 
	global denyList          
        for (src_mac, dst_mac) in denyList:
            match = of.ofp_match()
            match.dl_src = src_mac
            match.dl_dst = dst_mac
            msg = of.ofp_flow_mod()
            msg.match = match
            event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch (firewall_config="policies.csv"):
	global denyList
	with open(firewall_config, 'rb') as config:
            MacList = csv.DictReader(config)
            for row in MacList:               
		denyList.append((EthAddr(row['mac_0']),EthAddr(row['mac_1'])))
		denyList.append((EthAddr(row['mac_1']),EthAddr(row['mac_0'])))
	# Starting the Firewall
	core.registerNew(Firewall)
