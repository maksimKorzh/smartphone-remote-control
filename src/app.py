from flask import Flask
from flask import render_template_string
from flask import request
import socket

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

app = Flask(__name__)

@app.route('/')
def root():
    return render_template_string('''
        <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=0, maximum-scale=0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            <script
              src="https://code.jquery.com/jquery-3.6.0.min.js"
              integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
              crossorigin="anonymous">
            </script>
          </head>
          <body>
            <div class="btn-group d-flex" role="group" aria-label="...">
              <button id="left" type="button" class="w-100" style="height: 200px; background-color: #F0F0F0; font-size: 100px;">Left</button>
              <button id="right" type="button" class="w-100" style="height: 200px; background-color: #F0F0F0; font-size: 100px;">Right</button>
            </div>
            <input id="keyboard" type="text" class="w-100" placeholder="          Tap here to type text..." style="height: 200px; font-size: 100px;">
            <div id="touchpad" style="display:flex; width: 100%; height: 100%; background-color: black"></div>
            <script>
              var curX = 0;
              var curY = 0;
              var oldX = curX;
              var oldY = curY;
              var move = false;
              var offsetX = 0;
              var offsetY = 0;
              var mouseLock = 0;
              
              function getPosition() {
                curX = Math.floor(event.targetTouches[0].clientX);
                curY = Math.floor(event.targetTouches[0].clientY);
              }
              
              function updatePosition() {
                oldX = curX;
                oldY = curY;
                curX = Math.floor(event.targetTouches[0].clientX);
                curY = Math.floor(event.targetTouches[0].clientY);
   
                if (curX > oldX) offsetX = curX - oldX;
                if (curX < oldX) offsetX = -(oldX - curX);
                if (curY > oldY) offsetY = curY - oldY;
                if (curY < oldY) offsetY = -(oldY - curY);
              }

              document.getElementById('keyboard').onkeyup = function(event) {
                let key = '';
                switch(event.keyCode) {
                  case 13: key = 'newline'; break;
                  case 8: key = 'backspace'; break;
                  default: key = this.value.slice(-1) == ' ' ? 'space' : this.value.slice(-1); break;
                }
                $.post('/keyboard', {'key': key});
                this.value = '';
              }
              
              document.getElementById('left').onclick = function() {
                mouseLock ^= 1;
                if (mouseLock) {
                  $.post('/mousedown');
                  document.getElementById('left').style.backgroundColor = 'red';
                } else {
                  $.post('/mouseup');
                  document.getElementById('left').style.backgroundColor = '#F0F0F0';
                }
              }
              
              document.getElementById('right').onclick = function() {
                $.post('/rightclick');
              }
              
              document.getElementById('touchpad').onclick = function() {
                $.post('/click');
              }
                            
              document.getElementById('touchpad').ontouchstart = function(event) {
                getPosition();
                move = true;
              }
              
              document.getElementById('touchpad').ontouchmove = function(event) {
                event.preventDefault();
                updatePosition();
                
                $.post('/move', {
                  'offsetX': move ? (offsetX => 0 ? 1 : -1) : offsetX,
                  'offsetY': move ? (offsetY => 0 ? 1 : -1) : offsetY
                });
                
                move = false;
              }
              
            </script>
          </body>
        </html>
    ''')

@app.route('/click', methods=['POST'])
def click():
    UDPClientSocket.sendto( str.encode('click'), ('127.0.0.1', 20001))
    return 'Done'

@app.route('/move', methods=['POST'])
def control():
    offsetX = request.form.get('offsetX')
    offsetY = request.form.get('offsetY')
    
    print(offsetX, offsetY)
    
    # Send to server using created UDP socket
    UDPClientSocket.sendto( str.encode('move ' + offsetX + ' ' + offsetY), ('127.0.0.1', 20001))

    return 'Done'

@app.route('/drag', methods=['POST'])
def drag():
    offsetX = request.form.get('offsetX')
    offsetY = request.form.get('offsetY')
    
    print(offsetX, offsetY)
    
    # Send to server using created UDP socket
    UDPClientSocket.sendto( str.encode('drag ' + offsetX + ' ' + offsetY), ('127.0.0.1', 20001))
    
    return 'Done'

@app.route('/mousedown', methods=['POST'])
def mousedown():
    UDPClientSocket.sendto( str.encode('mousedown'), ('127.0.0.1', 20001))
    return 'Done'

@app.route('/mouseup', methods=['POST'])
def mouseup():
    UDPClientSocket.sendto( str.encode('mouseup'), ('127.0.0.1', 20001))
    return 'Done'

@app.route('/rightclick', methods=['POST'])
def rigthclick():
    UDPClientSocket.sendto( str.encode('rightclick'), ('127.0.0.1', 20001))
    return 'Done'

@app.route('/keyboard', methods=['POST'])
def keyboard():
    print(request.form)
    key = request.form.get('key')
    UDPClientSocket.sendto( str.encode('keypress ' + (key if key != ' ' else 'space')), ('127.0.0.1', 20001))
    return 'Done'


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
    
    
    
    
    
    
    
    
    
    
    
    
