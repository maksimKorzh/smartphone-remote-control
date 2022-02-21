import socket
import pyautogui

pyautogui.FAILSAFE = False
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('127.0.0.1', 20001))
print("UDP server up and listening")

x, y = pyautogui.position()
posX = x
posY = y

def update_position(offsetX, offsetY):
    global posX, posY
    x, y = pyautogui.position()
    posX = x
    posY = y
    posX += int(offsetX)
    posY += int(offsetY)

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(1024)
    command = bytesAddressPair[0].decode().split()
    event = command[0]    

    if event == 'click':
        pyautogui.click()
        print('Click:', posX, posY)
    
    if event == 'rightclick':
        pyautogui.click(button='right')
        print('Right click:', posX, posY)

    if event == 'move':
        update_position(command[1], command[2])
        pyautogui.moveTo(posX, posY, _pause=False)
        print('Move:', posX, posY)

    if event == 'mousedown':
        pyautogui.mouseDown()
        print('Mouse down')
    
    if event == 'mouseup':
        pyautogui.mouseUp()
        print('Mouse up')

    if event == 'keypress':
        try:
            print('Pressed "' + command[1] + '"')
            if command[1] == 'newline': pyautogui.press('return');
            elif command[1] == 'backspace': pyautogui.press('backspace');
            elif command[1] == 'space': pyautogui.press(' ');
            else: pyautogui.press(command[1])
        
        except:
            pass


