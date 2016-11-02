#!/usr/bin/python

import sys,csv,socket,csv

if len(sys.argv) == 2:   #To see if this is a put request
	filename=sys.argv[1]
	print filename

if len(sys.argv) == 3:	#To see if this is a rename request
	original_filename=sys.argv[1]
	new_filename=sys.argv[2]

with open("/home/amisanghavi/mininet/server2/serverlist.csv", 'rb') as f:
     reader = csv.DictReader(f)
     for row in reader:
	s = socket.socket() 
     	server_ip=(row['server_ip'])
	host_ip=(row['server_port'])
	print server_ip
	print host_ip
	s.connect((server_ip, int(host_ip)))
	print "Connecting"
	print len(sys.argv) == 2
	print len(sys.argv)
	if len(sys.argv) == 2:
		print "Here 1"
		s.send("1")
		s.send(filename)
		f = open(filename,'rb')
		l = f.read(1024)
		while (l):
		       s.send(l)
		       print('Sent ',repr(l))
		       l = f.read(1024)
		f.close()
	if len(sys.argv) == 3:
		print "Here 2"
		s.send("2")
		s.send(original_filename+"\n")
		s.send(new_filename)
        s.close()
		


