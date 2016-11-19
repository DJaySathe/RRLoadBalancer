# For LoadBalancer code
copy LoadBalancer.py from 
https://github.com/asangha/IP573_asangha/tree/master/Code
and paste this code in forwarding folder inside your pox

copy input.txt from 
https://github.com/asangha/IP573_asangha/tree/master/Code
and paste this file in pox folder from where you will run the ./pox command
or you can create any file in same format as input.txt and place it in pox folder and specify the name in command below.

To run the load balancer code use command 

./pox.py forwarding.l2_learning misc.firewall forwarding.LoadBalance --virtual_ip=10.0.0.5 --virtual_mac=00:00:00:00:00:04 --server_config="input.txt"

where 
virtual_ip
virtual_mac
server_config 

are parameters and can be modified dynamically as per requirement.
