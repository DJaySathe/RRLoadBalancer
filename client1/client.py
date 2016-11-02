import socket                   # Import socket module
import sys

s = socket.socket()             # Create a socket object
host = "10.0.0.5"    # Get local machine name
port = 60001                    # Reserve a port for your service.

s.connect((host, port))
filename=sys.argv[1]
print filename
s.send(filename)

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
print('Successfully get the file')
s.close()
print('connection closed')
