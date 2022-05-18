from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pigpio 
from pigpio_dht import DHT11 
from time import sleep
import threading 

DHT11_PIN = 5
sensor = DHT11(DHT11_PIN)
sidste_temp = None
app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('hent_temp')
def hent_temp():
    sleep(0.5)
    socketio.emit('temp', sidste_temp)

@app.route('/')
def index():
    return render_template('index5.html')

def read_temp():
    global sidste_temp
    while True:
        sleep(2)
        try:
            sidste_temp = sensor.read()
        except:
            sidste_temp = None

temp_thread = threading.Thread(target=read_temp)
temp_thread.start()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)