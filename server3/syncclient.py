#!/usr/bin/python

import sys,csv,socket,csv,os

if sys.argv[1] == "put":   #To see if this is a put request
	filename=sys.argv[2]
	print filename
	option=1

if sys.argv[1] == "rename":	#To see if this is a rename request
	original_filename=sys.argv[2]
	new_filename=sys.argv[3]
	option=2

if sys.argv[1] == "delete":
	deleted_filename=sys.argv[2]
	option=3

cwd = os.getcwd()
print cwd
path = os.path.join(cwd, "serverlist.csv")
os.system(path)

with open(path, 'rb') as f:
     reader = csv.DictReader(f)
     for row in reader:
	s = socket.socket() 
     	server_ip=(row['server_ip'])
	host_ip=(row['server_port'])
	print server_ip
	print host_ip
	s.connect((server_ip, int(host_ip)))
	print "Connecting"
	if option == 1:
		print "Here 1"
		s.send("1")
		s.send(filename)
		print filename
		status=s.recv(2)
		with open((cwd+"/"+filename),'rb+') as z:
			l = z.read(1024)
			while (l):
			      	s.send(l)
			      	print('Sent ',repr(l))
			      	l = z.read(1024)
			z.close()
	if option == 2:
		print "Here 2"
		s.send("2")
		s.send(original_filename+"\n")
		s.send(new_filename)
	if option == 3:
		print "Here 3"
		s.send("3")
		s.send(deleted_filename)
        s.close()

