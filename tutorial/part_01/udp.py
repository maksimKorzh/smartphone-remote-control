#
# UDP server imitating mouse move/click
#     events and keyboard strokes
#

# packages
import socket

# create UDP server socket
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind the server socket to IP address and port
server_socket.bind(('127.0.0.1', 20001))

# print intro message
print('UDP server is up and running')

# listen to incoming datagrams
while(True):
    # receive datagram
    data = server_socket.recvfrom(1024)[0].decode()
    
    # extract headers
    headers = server_socket.recvfrom(1024)[1]
    ip = headers[0]
    port = headers[1]
    
    # print connection debug info
    #print('IP:', ip, ' PORT:', port)
    
    print(data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
