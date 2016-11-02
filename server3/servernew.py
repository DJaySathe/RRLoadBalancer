import socket,sys,os                   # Import socket module
port = 60001                   # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = "10.0.0.4"    # Get local machine name
print host
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print 'Server 3 listening....'

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = conn.recv(1024)
    print('Server received', repr(data))
    print data

    option=data[:1]
    print option
    print option=="3"
	
    


    if option=="1":
	    print("Inside Servers get")
	    filename=conn.recv(1024)
	    f = open(filename,'rb')
            l = f.read(1024)
	    while (l):
		       conn.send(l)
		       print('Sent ',repr(l))
		       l = f.read(1024)
            f.close()
	    
	    

            print('Done sending')
	    conn.send('Thank you for connecting')
	    conn.close()
    
    if option=="2":
	print("Inside Servers put")
	filename=conn.recv(1024)
	with open(filename, 'wb') as f:
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
	os.system("/home/amisanghavi/mininet/server3/hello.py"+" "+filename)
	

    if option=="3":
	print "Inside listf"
	myList=os.listdir("/home/amisanghavi/mininet/server3")
	for i in range(len(myList)):
		conn.send(myList[i])
	conn.close()
	

	
    if option=="4":
	print "Inside rename"
	original_filename=conn.recv(1024)
	print original_filename
	new_filename=conn.recv(1024)
	print new_filename
	os.rename(original_filename,new_filename)
	os.system("/home/amisanghavi/mininet/server3/hello.py"+" "+original_filename+" "+new_filename)
	conn.close()
 	
 
	 
	

	
	
	




