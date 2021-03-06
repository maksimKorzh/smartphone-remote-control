#
# HTTP server + UDP client for user inpt handling
#

# packages
from flask import Flask
from flask import render_template_string
from flask import request

# create app instance
app = Flask(__name__)

# home page
@app.route('/')
def root():
    return render_template_string('''
      <html>
        <head>
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
          <!-- Touchpad -->
          <div id="touchpad" style="display: flex; width: 100%; height: 100%; background-color: black"></div>
        </body>
        <script>
          // listen to touch move event
          document.getElementById('touchpad').ontouchmove = function(event) {
            // prevent scrolling smartphone browser
            event.preventDefault()
            
            // send touch move offset coords to the API
            $.post('/move',
            {
              'offsetX': offsetX,
              'offsetY': offsetY
            })
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
    
    print(offsetX, offsetY)    
    return 'Done'


# start HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)












