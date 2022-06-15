#!/usr/bin/python3
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
import time
import os

if'__main__'==__name__:
	os.system('mn -c')
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)

	#Build Topology
	HostA = net.addHost('HostA')
	HostB = net.addHost('HostB')
	R1 = net.addHost('R1')
	R2 = net.addHost('R2')
	R3 = net.addHost('R3')
	R4 = net.addHost('R4')

	#Mendefinisikan bandwidth (/Mbps)
	bandwidth1={'bw':1}
	bandwidth2={'bw':0.5}

	#Menghubungkan antar device
	net.addLink(HostA,R1,cls=TCLink, **bandwidth1) #HostA-eth0 R1-eth0
	net.addLink(HostA,R2,cls=TCLink, **bandwidth1) #HostA-eth1 R2-eth0

	net.addLink(HostB,R3,cls=TCLink, **bandwidth1) #HostB-eth0 R3-eth0
	net.addLink(HostB,R4,cls=TCLink, **bandwidth1) #HostB-eth1 R4-eth0

	net.addLink(R1,R3,cls=TCLink, **bandwidth2) #R1-eth1 R3-eth1
	net.addLink(R1,R4,cls=TCLink, **bandwidth1) #R1-eth2 R4-eth1

	net.addLink(R2,R3,cls=TCLink, **bandwidth1) #R2-eth1 R3-eth2
	net.addLink(R2,R4,cls=TCLink, **bandwidth2) #R2-eth2 R4-eth2

	net.build()

	#define NIC on each host
	HostA.cmd("ifconfig HostA-eth0 0")
	HostA.cmd("ifconfig HostA-eth1 0")
		
	HostB.cmd("ifconfig HostB-eth0 0")
	HostB.cmd("ifconfig HostB-eth1 0")
		
	R1.cmd("ifconfig R1-eth0 0")
	R1.cmd("ifconfig R1-eth1 0")
	R1.cmd("ifconfig R1-eth2 0")
		
	R2.cmd("ifconfig R2-eth0 0")
	R2.cmd("ifconfig R2-eth1 0")
	R2.cmd("ifconfig R2-eth2 0")
		
	R3.cmd("ifconfig R3-eth0 0")
	R3.cmd("ifconfig R3-eth1 0")
	R3.cmd("ifconfig R3-eth2 0")
		
	R4.cmd("ifconfig R4-eth0 0")
	R4.cmd("ifconfig R4-eth1 0")
	R4.cmd("ifconfig R4-eth2 0")
		
	R1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	R2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	R3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	R4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
		
	#inisialisasi IP Address pada Interface setiap perangkat
	HostA.cmd("ifconfig HostA-eth0 192.168.10.1 netmask 255.255.255.0")
	HostA.cmd("ifconfig HostA-eth1 192.168.20.1 netmask 255.255.255.0")
	
	HostB.cmd("ifconfig HostB-eth0 192.168.30.1 netmask 255.255.255.0")
	HostB.cmd("ifconfig HostB-eth1 192.168.40.1 netmask 255.255.255.0")
	
	R1.cmd("ifconfig R1-eth0 192.168.10.2 netmask 255.255.255.0")
	R1.cmd("ifconfig R1-eth1 192.168.50.1 netmask 255.255.255.0")
	R1.cmd("ifconfig R1-eth2 192.168.70.1 netmask 255.255.255.0")
	
	R2.cmd("ifconfig R2-eth0 192.168.20.2 netmask 255.255.255.0")
	R2.cmd("ifconfig R2-eth1 192.168.80.1 netmask 255.255.255.0")
	R2.cmd("ifconfig R2-eth2 192.168.60.1 netmask 255.255.255.0")
	
	R3.cmd("ifconfig R3-eth0 192.168.30.2 netmask 255.255.255.0")
	R3.cmd("ifconfig R3-eth1 192.168.50.2 netmask 255.255.255.0")
	R3.cmd("ifconfig R3-eth2 192.168.80.2 netmask 255.255.255.0")
	
	R4.cmd("ifconfig R4-eth0 192.168.40.2 netmask 255.255.255.0")
	R4.cmd("ifconfig R4-eth1 192.168.70.2 netmask 255.255.255.0")
	R4.cmd("ifconfig R4-eth2 192.168.60.2 netmask 255.255.255.0")
	
	#Routing setiap perangkat yang bertetangga
	HostA.cmd("ip rule add from 192.168.10.1 table 1")
	HostA.cmd("ip rule add from 192.168.20.1 table 2")
	HostA.cmd("ip route add 192.168.10.0/24 dev HostA-eth0 scope link table 1")
	HostA.cmd("ip route add default via 192.168.10.2 dev HostA-eth0 table 1")
	HostA.cmd("ip route add 192.168.20.0/24 dev HostA-eth1 scope link table 2")
	HostA.cmd("ip route add default via 192.168.20.2 dev HostA-eth1 table 2")
	HostA.cmd("ip route add default scope global nexthop via 192.168.10.2 dev HostA-eth0")
	
	HostB.cmd("ip rule add from 192.168.30.1 table 1")
	HostB.cmd("ip rule add from 192.168.40.1 table 2")
	HostB.cmd("ip route add 192.168.30.0/24 dev HostB-eth0 scope link table 1")
	HostB.cmd("ip route add default via 192.168.30.2 dev HostB-eth0 table 1")
	HostB.cmd("ip route add 192.168.40.0/24 dev HostB-eth1 scope link table 2")
	HostB.cmd("ip route add default via 192.168.40.2 dev HostB-eth1 table 2")
	HostB.cmd("ip route add default scope global nexthop via 192.168.30.2 dev HostB-eth0")

	R1.cmd("ip rule add from 192.168.10.2 table 1")
	R1.cmd("ip rule add from 192.168.50.1 table 2")
	R1.cmd("ip rule add from 192.168.70.1 table 3")
	R1.cmd("ip route add 192.168.10.0/24 dev R1-eth0 scope link table 1")
	R1.cmd("ip route add default via 192.168.10.1 dev R1-eth0 table 1")
	R1.cmd("ip route add 192.168.50.0/24 dev R1-eth1 scope link table 2")
	R1.cmd("ip route add default via 192.168.50.2 dev R1-eth1 table 2")
	R1.cmd("ip route add 192.168.70.0/24 dev R1-eth2 scope link table 3")
	R1.cmd("ip route add default via 192.168.70.2 dev R1-eth2 table 3")
	R1.cmd("ip route add default scope global nexthop via 192.168.10.1 dev R1-eth0")
	
	R2.cmd("ip rule add from 192.168.20.2 table 1")
	R2.cmd("ip rule add from 192.168.80.1 table 2")
	R2.cmd("ip rule add from 192.168.60.1 table 3")
	R2.cmd("ip route add 192.168.20.0/24 dev R2-eth0 scope link table 1")
	R2.cmd("ip route add default via 192.168.20.2 dev R2-eth0 table 1")
	R2.cmd("ip route add 192.168.80.0/24 dev R2-eth1 scope link table 2")
	R2.cmd("ip route add default via 192.168.80.2 dev R2-eth1 table 2")
	R2.cmd("ip route add 192.168.60.0/24 dev R2-eth2 scope link table 3")
	R2.cmd("ip route add default via 192.168.60.2 dev R2-eth2 table 3")
	R2.cmd("ip route add default scope global nexthop via 192.168.20.2 dev R2-eth0")
	
	R3.cmd("ip rule add from 192.168.30.2 table 1")
	R3.cmd("ip rule add from 192.168.50.2 table 2")
	R3.cmd("ip rule add from 192.168.80.2 table 3")
	R3.cmd("ip route add 192.168.30.0/24 dev R3-eth0 scope link table 1")
	R3.cmd("ip route add default via 192.168.30.1 dev R3-eth0 table 1")
	R3.cmd("ip route add 192.168.50.0/24 dev R3-eth1 scope link table 2")
	R3.cmd("ip route add default via 192.168.50.1 dev R3-eth1 table 2")
	R3.cmd("ip route add 192.168.80.0/24 dev R3-eth2 scope link table 3")
	R3.cmd("ip route add default via 192.168.80.1 dev R3-eth2 table 3")
	R3.cmd("ip route add default scope global nexthop via 192.168.30.1 dev R3-eth0")
	
	R4.cmd("ip rule add from 192.168.40.2 table 1")
	R4.cmd("ip rule add from 192.168.70.2 table 2")
	R4.cmd("ip rule add from 192.168.60.2 table 3")
	R4.cmd("ip route add 192.168.40.0/24 dev R4-eth0 scope link table 1")
	R4.cmd("ip route add default via 192.168.40.1 dev R4-eth0 table 1")
	R4.cmd("ip route add 192.168.70.0/24 dev R4-eth1 scope link table 2")
	R4.cmd("ip route add default via 192.168.70.1 dev R4-eth1 table 2")
	R4.cmd("ip route add 192.168.60.0/24 dev R4-eth2 scope link table 3")
	R4.cmd("ip route add default via 192.168.60.1 dev R4-eth2 table 3")
	R4.cmd("ip route add default scope global nexthop via 192.168.40.1 dev R4-eth0")
	
	#Membuat routing static
	R1.cmd("route add -net 192.168.30.0/24 gw 192.168.50.2")
	R1.cmd("route add -net 192.168.40.0/24 gw 192.168.70.2")
	R1.cmd("route add -net 192.168.60.0/24 gw 192.168.70.2")
	R1.cmd("route add -net 192.168.80.0/24 gw 192.168.50.2")
	
	R2.cmd("route add -net 192.168.30.0/24 gw 192.168.80.2")
	R2.cmd("route add -net 192.168.40.0/24 gw 192.168.60.2")
	R2.cmd("route add -net 192.168.50.0/24 gw 192.168.80.2")
	R2.cmd("route add -net 192.168.70.0/24 gw 192.168.60.2")
	
	R3.cmd("route add -net 192.168.10.0/24 gw 192.168.50.1")
	R3.cmd("route add -net 192.168.20.0/24 gw 192.168.80.1")
	R3.cmd("route add -net 192.168.60.0/24 gw 192.168.80.1")
	R3.cmd("route add -net 192.168.70.0/24 gw 192.168.50.1")
	
	R4.cmd("route add -net 192.168.10.0/24 gw 192.168.70.1")
	R4.cmd("route add -net 192.168.20.0/24 gw 192.168.60.1")
	R4.cmd("route add -net 192.168.50.0/24 gw 192.168.70.1")
	R4.cmd("route add -net 192.168.80.0/24 gw 192.168.60.1")
	
	R1.cmdPrint("tc qdisc del dev R1-eth0 root")
	R1.cmdPrint("tc qdisc add dev R1-eth0 root netem delay 20ms")
	
	#R2.cmdPrint("tc qdisc del dev R2-eth1 root")
	#R2.cmdPrint("tc qdisc add dev R2-eth1 root netem loss 20%")
	
	#R3.cmdPrint("tc qdisc del dev R3-eth0 root")
	#R3.cmdPrint("tc qdisc add dev R3-eth0 root netem delay 40ms")
	
	time.sleep(2)
	# run background traffic
	HostB.cmd("iperf -s &") #Buat server
	HostB.cmd("tcpdump -w test.pcap &") #Bikin file wireshark
	HostA.cmd("iperf -c 192.168.30.1 -t 100 &") #Buat client dan BEBAN HIDUP
	time.sleep(2)
	HostA.cmd("iperf -c 192.168.30.1") #BEBAN HIDUP
	
	CLI(net)
	
	net.stop()