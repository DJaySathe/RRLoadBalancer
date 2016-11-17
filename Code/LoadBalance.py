import fileinput 
import sys


#log = core.getLogger()

serverList = {}
file_name = sys.argv[1]
f = open(file_name)
data = f.readlines()
#print (data)
f.close()

i=0
for line in data:
    columns=line.split()
    #serverList[i]={'ip':IPAddr(columns[0]), 'mac':EthAddr(columns[1]), 'outport': columns[2]}
    serverList[i]={'ip':columns[0], 'mac':columns[1], 'outport': columns[2]}
    print (serverList[i])
    i=i+1
    
#virtual_ip = IPAddr(sys.argv[2])
#virtual_mac = EthAddr(sys.argv[3])
print (sys.argv[2])
print (sys.argv[3])

#Round Robin
ServerUsed = 0 
while (1):
   print ('The count is:', ServerUsed)
   ServerUsed = (ServerUsed + 1)% serverList.__len__()
   
