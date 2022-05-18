from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pigpio 
from time import sleep 

LED_GPIO_PIN = 26
pi = pigpio.pi() 
app = Flask(__name__)
socketio = SocketIO(app)
pi.set_PWM_range(LED_GPIO_PIN, 100)

@socketio.on('skru_fra_browser')
def skru(data):
    lysstyrke = int(data['lysstyrke'])
    if lysstyrke < 0:
        lysstyrke = 0
    if lysstyrke > 50:
        lysstyrke = 50
    pi.set_PWM_dutycycle(LED_GPIO_PIN, lysstyrke)
    
@app.route('/')
def index():
    return render_template('index3.html')
    
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)