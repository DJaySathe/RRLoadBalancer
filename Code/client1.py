import socket                   # Import socket module
import sys

s = socket.socket()             # Create a socket object
host = "192.168.203.144"    # Get local machine name
port = 60002                    # Reserve a port for your service.

s.connect((host, port))
response=input('Enter the operation you want to perform 1:Get 2:Put 3:ListallFiles 4:Changenameofthefile') #Get user input for the operation it wants to perform

s.send(str(response))

def put():
	print "put"
	filename=raw_input("Enter the filename to be put")
	s.send(filename)
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
	       s.send(l)
	       print('Sent ',repr(l))
	       l = f.read(1024)
	f.close()

def get():
	print "get"
	filename=raw_input("Enter the filename to be be retrieved")
	s.send(filename)
	print("Hey")
	with open(filename, 'wb') as f:
	    print 'file opened'
	    while True:
		print('receiving data...')
		data = s.recv(1024)
		print('data=%s', (data))
		if not data:
		    break
		# write data to a file
		f.write(data)
	f.close()

def listf():
	print "listf"
        while True:
		print('receiving data...')
		data=s.recv(1024)
		print('data=%s', (data))
		if not data:
			break
				

def rename():
	print "rename"
	original_filename=raw_input("Enter the original filename")
	s.send(original_filename)
	new_filename=raw_input("Enter the new filename")
	s.send(new_filename)

options = {1 : get, 2 : put, 3 : listf, 4 : rename,
}
options[response]()


print('Successfully get the file')
s.close()
print('connection closed')
