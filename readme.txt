* Environment settings


1. It is better to use Ubuntu OS for mininet environment as they also support newest OpenVswitch. To install mininet :


→ git clone git://github.com/mininet/mininet
→ cd mininet
→ git tag  # list available versions
→ git checkout -b 2.2.1 2.2.1  # or whatever version you wish to install
→ cd ..
→ mininet/util/install.sh


      2) We create our mininet topology. It  can be either created as a python file or sh file. We created sh file ‘createtopology.sh’. Traverse where mininet folder is present and save the topology file there. Then test our topology


→ cd mininet
→ ./createtopology.sh
→ pingall

         3) Now setup the dataplane environment. Mininet only virtualizes the network space, not the address space. So on the basis of one paper, we made all servers reside in different folders to demonstrate that they are virtualized completely. We have three servers and a client,  trace the folder mininet, and create different folder for individual servers viz. server1, server2, server3. So that the network is fully virtualised. Each server will have server.py,syncclient.py and syncserver.py 
Syncclient is basically used to sync files to other servers whenever a put request comes




          4) After dataplane environment we come to the control plane environment. Here  implement the controller code. For simplicity we created different service modules that can be simultaneously run on the controller. In our case, there will be three service modules for L2_learning, Load balancing, firewall.


→ cd mininet/pox/forwarding
Place the executable service modules and ‘Load_Balancer.py’ here.
We have used the default L2_learning module available in POX folder.


→ cd ../misc
Place the executable service module ‘firewall.py’ here. 
And firewall polices - List of all Dest Ip that should be drop.


* How to run the code :


1. First run the pox controller. Go to the folder where pox folder is stored as pox folder contains mandatory executable pox controller python code.


→ cd mininet/pox


Then run this controller code along with execution of various service modules by defining the path and required input files. (virtual ip, virtual mac, policies.csv, input.txt)


→ ./pox.py forwarding.l2_learning misc.firewall --firewall_config=”policies.csv” forwarding.Load_Balancer --virtual_ip=10.0.0.5 --virtual_mac=00.00.00.00.00.04 --server_config=”input.txt”


    2) Then run the topology file that was created.


→ cd mininet
→ ./createtopology.sh


3)


Terminal where the mininet topology is run will show like this ;


mininet >


Ipconfig - shows different IPs and
Ls - Shows its own files
So we need to start the server and client instances at 4 different locations. (3 for server and one for client). Start the 4 xterm terminals viz. h1,h2,h3,h4 


mininet> xterm h1 h2 h3 h4 


Starting the servers for h2 h3 h4 
go to respective folders(server1/server2/server3) in xterm
→ cd server1
→ cd server2
→ cd server3
→ cd server4


And run
→  python server.py 
in each one.


For making a request from client go to folders client1/client2 in xterm run
→ python client.py






* How to interpret the results


We have implemented logs in clients,flow tables,and pox controller. So results can be verified by observing logs.
Client logs will display at each level which server it was connected to.
Flow tables will show various entries where it is destined to . Also pox controller will show where the client gets connected to at each request


Sample input and output files


We provide same RFC files (RFC 1000, RFC 2000, RFC 3456) on the servers (All servers should have the same files). Client will have (RFC 1500, RFC 5000) and they will be put on the server.