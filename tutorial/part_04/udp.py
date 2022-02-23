#
# UDP server imitating mouse move/click
#     events and keyboard strokes
#

# packages
import socket
import pyautogui

# create UDP server socket
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind the server socket to IP address and port
server_socket.bind(('127.0.0.1', 20001))

# print intro message
print('UDP server is up and running')

# mouse pointer coords
posX = 0;
posY = 0;

# allow moving mouse off screen
pyautogui.FAILSAFE = False

# listen to incoming datagrams
while(True):
    # receive datagram
    data = server_socket.recvfrom(1024)[0].decode().split(' ')
    
    # parse command
    event = data[0]
    offsetX = int(data[1])
    offsetY = int(data[2])
    
    # extract headers
    headers = server_socket.recvfrom(1024)[1]
    ip = headers[0]
    port = headers[1]
    
    # print connection debug info
    #print('IP:', ip, ' PORT:', port)

    # handle mouse move command
    if event == 'move':
        # get current mouse pointer coordinates
        posX, posY = pyautogui.position()
        
        # adjust mouse pointer position
        posX += offsetX
        posY += offsetY
        
        # mimic mouse move to the new position
        pyautogui.moveTo(posX, posY, _pause=False)
    
    print(event, offsetX, offsetY)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
