#!/usr/bin/python
import socket,sys,os                   # Import socket module

port = 60040                   # Reserve a port for your service.
s = socket.socket()             # Create a socket object
#host = "10.0.0.2"    # Get local machine name
#print host
s.bind(('', port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
print ("Sync Server Connected")

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = conn.recv(1)
    print('Server received', repr(data))
    print data

    option=data[:1]
    print option

    if option=="1":
   	    print("Inside Servers Syncserver 1 put")
	    filename = conn.recv(1024)
	    conn.send("OK")
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

    if option=="2":
	    full_filename=conn.recv(1024)
	    strarr=full_filename.split( )
	    original_filename=strarr[0]
	    print "Ori"+original_filename
	    new_filename=strarr[1]
	    print "New"+new_filename
	    os.rename(original_filename,new_filename)
	    conn.close()

    if option=="3":
	    full_filename=conn.recv(1024)
	    os.remove(full_filename)
	    conn.close()

    		



