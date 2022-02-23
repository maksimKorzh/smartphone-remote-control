#
# HTTP server + UDP client for user input handling
#

# packages
from flask import Flask
from flask import render_template_string
from flask import request
import socket

# create UDP client socket
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# create app instance
app = Flask(__name__)

# home page
@app.route('/')
def root():
    return render_template_string('''
      <html>
        <head>
          <!-- avoid zooming on a tocuh device -->
          <meta name="viewport" content="width=device-width, initial-scale=0, maximum-scale=0">
          
          <!-- Bootstrap -->
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
          
          <!-- JQuery -->
          <script
             src="https://code.jquery.com/jquery-3.6.0.min.js"
             integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
             crossorigin="anonymous">
          </script>
        </head>
        <body>          
          <!-- Mouse buttons -->
          <div class="btn-group d-flex" role="group" aria-label="...">
            <button id="leftButton" type="button" class="w-100" style="height: 200px; background-color: #F0F0F0; font-size: 100px;">Left</button>
            <button id="rightButton" type="button" class="w-100" style="height: 200px; background-color: #F0F0F0; font-size: 100px;">Right</button>
          </div>
         
          <!-- Touchpad -->
          <div id="touchpad" style="display: flex; width: 100%; height: 100%; background-color: black"></div>
        </body>
        <script>
          // variables
          var curX = 0;
          var curY = 0;
          var oldX = 0;
          var oldY = 0;
          var offsetX = 0;
          var offsetY = 0;
          var moveFlag = false;
          var buttonLock = 0;
          
          // get current absolute X,Y position of the touch
          function getPosition(event) {
            curX = Math.floor(event.targetTouches[0].clientX);
            curY = Math.floor(event.targetTouches[0].clientY);
          }
          
          // get the relative offsets of the touch
          function getOffsets(event) {
            oldX = curX;
            oldY = curY;
            getPosition(event);
            
            if (curX > oldX) offsetX = curX - oldX;
            if (curX < oldX) offsetX = -(oldX - curX);
            if (curY > oldY) offsetY = curY - oldY;
            if (curY < oldY) offsetY = -(oldY - curY);
          }
          
          // listen to touch start event
          document.getElementById('touchpad').ontouchstart = function(event) {
            // get current X,Y touch coordinates
            getPosition(event);
            
            // toggle move flag
            moveFlag = true;
          }
          
          // listen to touch move event
          document.getElementById('touchpad').ontouchmove = function(event) {
            // prevent scrolling smartphone browser
            event.preventDefault()
            
            // get relative offsets
            getOffsets(event);
            
            // send touch move offset coords to the API
            $.post('/move',
            {
              'offsetX': moveFlag ? (offsetX >= 0 ? 1 : -1 ) : offsetX,
              'offsetY': moveFlag ? (offsetY >= 0 ? 1 : -1 ) : offsetY
            })
            
            // toggle move flag
            moveFlag = false
          }
          
          // listen to touchpad click event
          document.getElementById('touchpad').onclick = function(event) {
            $.post('/click')
          }
          
          // listen to right mouse button click event
          document.getElementById('rightButton').onclick = function(event) {
            $.post('/rightclick')
          }

          // listen to left mouse button toggling
          document.getElementById('leftButton').onclick = function(event) {
            // toggle button lock
            buttonLock ^= 1;
            
            // if mouse button is down
            if (buttonLock) {
              $.post('/mousedown');
              document.getElementById('leftButton').style.backgroundColor = 'red';
            } else {
              $.post('/mouseup');
              document.getElementById('leftButton').style.backgroundColor = '#F0F0F0';
            }
          }
        </script>
      <html>
    ''')

# move mouse pointer
@app.route('/move', methods=['POST'])
def move():
    # extract offsets
    offsetX = request.form.get('offsetX')
    offsetY = request.form.get('offsetY')
    
    # send UDP move message
    client_socket.sendto(str.encode('move ' + offsetX + ' ' + offsetY), ('127.0.0.1', 20001))
    
    return 'Done'

# click on touchpad
@app.route('/click', methods=['POST'])
def click():
    # send UDP click message
    client_socket.sendto(str.encode('click'), ('127.0.0.1', 20001))

    return 'Done'

# click right mouse button
@app.route('/rightclick', methods=['POST'])
def rigthclick():
    # send UDP click message
    client_socket.sendto(str.encode('rightclick'), ('127.0.0.1', 20001))
    
    return 'Done'

# press and hold left mouse button
@app.route('/mousedown', methods=['POST'])
def mousedown():
    # send UDP click message
    client_socket.sendto(str.encode('mousedown'), ('127.0.0.1', 20001))
    return 'Done'

# release left mouse button
@app.route('/mouseup', methods=['POST'])
def mouseup():
    # send UDP click message
    client_socket.sendto(str.encode('mouseup'), ('127.0.0.1', 20001))
    
    return 'Done'

# start HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)












