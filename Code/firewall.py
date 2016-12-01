from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
 
import csv
 
log = core.getLogger()
policyFile = "%s/mininet/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]
denyList={} 
''' Add your global variables here ... '''
def launch (firewall_config="policies.csv"):
	global denyList
	with open(firewall_config, 'rb') as config:
            MacList = csv.DictReader(config)
			i=0
            for row in MacList:
                denyList[i]={(EthAddr(row['mac_0']), EthAddr(row['mac_1'])}
                denyList[i+1]={((EthAddr(row['mac_1']), EthAddr(row['mac_0'])}
				print (denyList[i])
				i=i+2
				print (i)
 
class Firewall (EventMixin):
 
    def __init__ (self):
		global denyList
        self.listenTo(core.openflow)
        log.debug("Firewall Enabled")
        
    def _handle_ConnectionUp (self, event):    
        for (src_mac, dst_mac) in denyList:
            match = of.ofp_match()
            match.dl_src = src_mac
            match.dl_dst = dst_mac
            msg = of.ofp_flow_mod()
            msg.match = match
            event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
 
