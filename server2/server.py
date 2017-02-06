import socket,sys,os                   # Import socket module
port = 60001                   # Reserve a port for your service.
s = socket.socket()             # Create a socket object
#host = "10.0.0.2"    # Get local machine name
#print host

#Change only this lines for different server

cwd = os.getcwd()
print cwd
path = os.path.join(cwd, "syncserver.py&")
os.system(path)

path1= os.path.join(cwd, "syncclient.py")

s.bind(('', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.



print 'Server 2 listening....'



while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    conn.send("Connected to Server 2")
    data = conn.recv(1024)
    print('Server received', repr(data))
    
    print data

    option=data[:1]
    #print option
    #print option=="3"
	
    


    if option=="1":
	
	    print("Inside Servers get")
	    filename=conn.recv(1024)
	    if os.path.exists(filename):
		    status=200
		    conn.sendall(str(status))
		    print status
		    f = open(filename,'rb+')
		    l = f.read(1024)
		    while (l):
			       conn.send(l)
			       print('Sent ',repr(l))
			       l = f.read(1024)
		    f.close()
		    conn.close()
	    else:
	         conn.send("404")
		 print "File not found"
    
    if option=="2":
	print("Inside Servers put")
	filename=conn.recv(1024)
	print filename
	with open(filename, 'wb+') as f:
	    conn.send("OK")
	    print 'file opened'
	    while True:
		print('receiving data...')
		data = conn.recv(1024)
		print('data=%s', (data))
		if not data:
		    break
		# write data to a file
		f.write(data)
	f.close()
	os.system(path1+" "+"put"+" "+filename)
	

    if option=="3":
	print "Inside listf"
	
	myList=os.listdir(cwd)
	for i in myList:
		size=os.path.getsize(cwd+"/"+i)
		#print i+":"+str(size)
		#print i+":"+str(size)
	        if i.find(".py") == -1 : 
		  print i+":"+str(size)
		  conn.send('\n'+i+":"+str(size))
	conn.close()
	

	
    if option=="4":
	print "Inside rename"
	original_filename=conn.recv(1024)
	print original_filename
	new_filename=conn.recv(1024)
	print new_filename
	if os.path.exists(original_filename):
		    status=200
		    conn.send(str(status))
		    print status
		    os.rename(original_filename,new_filename)
		    os.system(path1+" "+"rename"+" "+original_filename+" "+new_filename)
		    conn.close()
	else:
	         conn.send("404")
		 print "File not found"

 	
    if option=="5":
	print "Inside delete"
	deleted_filename=conn.recv(1024)
	print deleted_filename
	if os.path.exists(deleted_filename):
		    status=200
		    conn.send(str(status))
		    print status
		    os.remove(deleted_filename)
		    os.system(path1+" "+"delete"+" "+deleted_filename)
		    conn.close()
	else:
		 conn.send("404")
		 print "File not found"
