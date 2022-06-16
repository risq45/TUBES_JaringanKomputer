#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.node import CPULimitedHost, Node, Controller
import os


class MyTopo ( Topo ):
	def __init__(self,**opts):
		Topo.__init__(self,**opts)
		
		#Add Host	
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')

		#Add Router
		r1 = self.addHost('r1',buffer=100)
		r2 = self.addHost('r2',buffer=100)
		r3 = self.addHost('r3',buffer=100)
		r4 = self.addHost('r4',buffer=100)

		#Add Host-Router Link
		self.addLink( 'h1' , 'r1', intfName1='h1-eth0', intfName2='r1-eth0' ,cls=TCLink , bw=1 ) 
		self.addLink( 'h1' , 'r2', intfName1='h1-eth1', intfName2='r2-eth1' ,cls=TCLink , bw=1 )
		self.addLink( 'h2' , 'r3', intfName1='h2-eth1', intfName2='r3-eth2' ,cls=TCLink , bw=1 )
		self.addLink( 'h2' , 'r4', intfName1='h2-eth0', intfName2='r4-eth0' ,cls=TCLink , bw=1 )

		#Add Router-Router Link
		self.addLink( 'r1' , 'r3', intfName1='r1-eth1', intfName2='r3-eth1', cls=TCLink , bw=0.5 )
		self.addLink( 'r1' , 'r4', intfName1='r1-eth2', intfName2='r4-eth1', cls=TCLink , bw=1 )
		self.addLink( 'r3' , 'r2', intfName1='r3-eth0', intfName2='r2-eth0', cls=TCLink , bw=1 )
		self.addLink( 'r2' , 'r4', intfName1='r2-eth2', intfName2='r4-eth2', cls=TCLink , bw=0.5 )

def run():
	os.system('mn -c')
	os.system( 'clear' )
	topo = MyTopo()
	net = Mininet(topo=topo, link=TCLink)
	net.start()

	h1, h2, r1, r2, r3, r4 = net.get('h1', 'h2', 'r1', 'r2', 'r3', 'r4')

	#Config IP h1 dan h2
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h1.cmd("ifconfig h1-eth0 192.168.1.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.4.1 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eth1 0")
	h2.cmd("ifconfig h2-eth0 192.168.6.1 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.5.1 netmask 255.255.255.0")

	#Config r1 hingga r4
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.1.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.2.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.7.2 netmask 255.255.255.0")
	r1.cmd("sysctl net.ipv4.ip_forward=1")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.3.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.4.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.8.2 netmask 255.255.255.0")
	r2.cmd("sysctl net.ipv4.ip_forward=1")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.3.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.2.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.5.2 netmask 255.255.255.0")
	r3.cmd("sysctl net.ipv4.ip_forward=1")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.6.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.7.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.8.1 netmask 255.255.255.0")
	r4.cmd("sysctl net.ipv4.ip_forward=1")
	
	#Static Routing untuk Host 1 dan 2
	h1.cmd("ip rule add from 192.168.1.1 table 1")
	h1.cmd("ip rule add from 192.168.4.1 table 2")
	h1.cmd("ip route add 192.168.1.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.1.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.4.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.4.2 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.1.2 dev h1-eth0")

	h2.cmd("ip rule add from 192.168.6.1 table 3")
	h2.cmd("ip rule add from 192.168.5.1 table 4")
	h2.cmd("ip route add 192.168.6.0/24 dev h2-eth0 scope link table 3")
	h2.cmd("ip route add default via 192.168.6.2 dev h2-eth0 table 3")
	h2.cmd("ip route add 192.168.5.0/24 dev h2-eth1 scope link table 4")
	h2.cmd("ip route add default via 192.168.5.2 dev h2-eth1 table 4")
	h2.cmd("ip route add default scope global nexthop via 192.168.6.2 dev h2-eth0")

	#Static Routing untuk Router 1 hingga 4
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.6.0/24 gw 192.168.7.1")
	r1.cmd("route add -net 192.168.8.0/24 gw 192.168.7.1")

	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.8.1")
	r2.cmd("route add -net 192.168.7.0/24 gw 192.168.8.1")
	r2.cmd("route add -net 192.168.6.0/24 gw 192.168.8.1")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.3.1")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.3.1")

	r3.cmd("route add -net 192.168.1.0/24 gw 192.168.2.1")
	r3.cmd("route add -net 192.168.7.0/24 gw 192.168.2.1")
	r3.cmd("route add -net 192.168.4.0/24 gw 192.168.3.2")
	r3.cmd("route add -net 192.168.8.0/24 gw 192.168.3.2")
	r3.cmd("route add -net 192.168.6.0/24 gw 192.168.2.1")

	r4.cmd("route add -net 192.168.3.0/24 gw 192.168.8.2")
	r4.cmd("route add -net 192.168.4.0/24 gw 192.168.8.2")
	r4.cmd("route add -net 192.168.5.0/24 gw 192.168.8.2")
	r4.cmd("route add -net 192.168.2.0/24 gw 192.168.7.2")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.7.2")
	
	# # Set Queue Discipline to CBQ
	info( '\n Queue Disicline :\n' )

	# # reset queue discipline
	r1.cmdPrint( 'tc qdisc del dev r1-eth0 root' ) 
	r2.cmdPrint('tc qdisc del dev r2-eth0 root')
	r3.cmdPrint('tc qdisc del dev r3-eth0 root')
	r4.cmdPrint('tc qdisc del dev r4-eth0 root')

	# # add queue discipline root here
	info('\n QUEUE Disicline : CBQ\n')
	r1.cmdPrint('tc qdisc add dev r1-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
	r2.cmdPrint('tc qdisc add dev r2-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
	r3.cmdPrint('tc qdisc add dev r3-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')
	r4.cmdPrint('tc qdisc add dev r4-eth0 root handle 1: cbq rate 10Mbit avpkt 1000')

	r1.cmdPrint('tc class add dev r1-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
	r1.cmdPrint('tc filter add dev r1-eth0 parent 1: protocol ip u32 match ip src '+ h1.IP()+' flowid 1:1')
	r2.cmdPrint('tc class add dev r2-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
	r2.cmdPrint('tc filter add dev r2-eth0 parent 1: protocol ip u32 match ip src '+ h1.IP()+' flowid 1:1')
	r3.cmdPrint('tc class add dev r3-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
	r3.cmdPrint('tc filter add dev r3-eth0 parent 1: protocol ip u32 match ip src '+ h2.IP()+' flowid 1:1')
	r4.cmdPrint('tc class add dev r4-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded')
	r4.cmdPrint('tc filter add dev r4-eth0 parent 1: protocol ip u32 match ip src '+ h2.IP()+' flowid 1:1')

	info('\n')

	# # add queue dicipline classes here 
	r1.cmdPrint('tc class add dev r1-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
	r2.cmdPrint('tc class add dev r2-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
	r3.cmdPrint('tc class add dev r3-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )
	r4.cmdPrint('tc class add dev r4-eth0 parent 1: classid 1:1 cbq rate 5Mbit avpkt 1000 bounded' )


	# # add queue dicipline filters
	r1.cmdPrint( 'tc filter add dev r1-eth0 parent 1: protocol ip u32 match ip src '+h1.IP()+' flowid 1:1' ) 
	r2.cmdPrint( 'tc filter add dev r2-eth0 parent 1: protocol ip u32 match ip src '+h1.IP()+' flowid 1:1' ) 
	r3.cmdPrint( 'tc filter add dev r3-eth0 parent 1: protocol ip u32 match ip src '+h2.IP()+' flowid 1:1' ) 
	r4.cmdPrint( 'tc filter add dev r4-eth0 parent 1: protocol ip u32 match ip src '+h2.IP()+' flowid 1:1' ) 
	r1.cmdPrint( 'tc qdisc show dev r1-eth0' )
	r2.cmdPrint( 'tc qdisc show dev r2-eth0' )
	r3.cmdPrint( 'tc qdisc show dev r3-eth0' )
	r4.cmdPrint( 'tc qdisc show dev r4-eth0' )
	info('\n')

	CLI(net)
	net.stop()

if __name__ == '__main__':
	run()
	setLogLevel('info')

topos = { 'mytopo': ( lambda: MyTopo() ) }
