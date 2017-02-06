import socket                   # Import socket module
import sys,os

s = socket.socket()             # Create a socket object
host = "10.0.0.5"    		# Get local machine name
port = 60001                    # Reserve a port for your service.

#Adding arp entry to the virtual server 
#os.system("arp -s 10.0.0.5 00:00:00:00:00:05")

#Get user input for the operation it wants to perform
response=input('Enter the operation you want to perform\n 1:Get\n 2:Put\n 3:List Files\n 4:Rename File\n 5:Delete File\n') 

def connect():
	s.connect((host, port))
	servermsg=s.recv(1024)
	print servermsg
	s.send(str(response))


def put():
	#connect()
	print "put"
	filename=raw_input("Enter the filename to be uploaded to the server")
	print filename
	
	if os.path.exists(filename):
		connect()
		s.sendall(filename)
		status=s.recv(2)
		print status
	
		f = open(filename,'rb+')
		l = f.read(1024)
		print l
		while (l):
		       s.send(l)
		       print('Sent ',repr(l))
		       l = f.read(1024)
		f.close()
		print('Successfully performed the required operation')
		s.close()
		print('connection closed')
	else:
		print ('File not found')

def get():
	print "get"
	connect()
	
	filename=raw_input("Enter the filename to be be retrieved from the server")
	s.sendall(filename)
	status=s.recv(3)
	print status
	if status=="404":
		print "404 : Error : File not found"
	else :
		with open(filename, 'wb+') as f:
		    print '200 : OK'
		    while True:
			print('receiving data...')
			data = s.recv(1024)
			print('data=%s', (data))
			if not data:
			    break
			# write data to a file
			f.write(data)
		f.close()
	print('Successfully performed the required operation')
	s.close()
	print('connection closed')


def listf():
	connect()
	print('List of files in this server')
        while True:
		data=s.recv(1024)
		print data
		if not data:
			break
	print('Successfully performed the required operation')
	s.close()
	print('connection closed')


def rename():
	connect()
	print "rename"
	original_filename=raw_input("Enter the original filename")
	s.send(original_filename)
	new_filename=raw_input("Enter the new filename")
	s.send(new_filename)
	status=s.recv(3)
	print status
	if status=="404":
		print "404 : Error : File not found"
	else :
		print "Successfully renamed the file"
		#os.rename(original_filename,new_filename)
	print('Successfully performed the required operation')
	s.close()
	print('connection closed')


def delete():
	connect()
	print "Deleting"
	deleted_filename=raw_input("Enter the filename to be deleted")
	s.send(deleted_filename)
	status=s.recv(3)
	print status
	if status=="404":
		print "404 : Error : File not found"
	else :
		print "Successfully deleted the file"
	print('Successfully performed the required operation')
	s.close()
	print('connection closed')

options = {1 : get, 2 : put, 3 : listf, 4 : rename, 5 : delete
}
options[response]()


