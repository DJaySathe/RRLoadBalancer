"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

#Reference : Taken from sample topology file provided by Mininet

from mininet.topo import Topo
from mininet.net import Mininet

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."


        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        firstClient = self.addHost( 'h1' )
        firstServer = self.addHost( 'h2' )
	secondServer = self.addHost( 'h3' )
	thirdServer = self.addHost( 'h4' )
		

        leftSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( firstClient, leftSwitch )
        self.addLink( firstServer, leftSwitch )
	self.addLink( secondServer, leftSwitch )
	self.addLink( thirdServer, leftSwitch )
	

	

topos = { 'mytopo': ( lambda: MyTopo() ) }
