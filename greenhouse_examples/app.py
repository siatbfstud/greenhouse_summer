from flask import Flask, redirect, render_template
from flask_socketio import SocketIO, emit
from time import sleep
from pigpio_dht import DHT11 
import pigpio, smbus, threading

BUT_PIN = 4
DHT11_PIN = 5
LED_PIN = 27

app = Flask(__name__)

sensor = DHT11(DHT11_PIN)
sidste_temp = None
soil_percent = None

pi = pigpio.pi()
pi.set_PWM_range(LED_PIN, 100)
pi.set_PWM_frequency(LED_PIN, 100000)
socketio = SocketIO(app)

pi.set_mode(27, pigpio.OUTPUT)
bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x49# default address

def skift(gpio, level, tick):
    socketio.emit("skift", {"tilstand": level})

pi.callback(BUT_PIN, pigpio.EITHER_EDGE, skift)

@socketio.on('skru_fra_browser')
def skru(data):
    lysstyrke = int(data['lysstyrke'])
    if lysstyrke < 0:
        lysstyrke = 0
    if lysstyrke > 50:
        lysstyrke = 50
    pi.set_PWM_dutycycle(LED_PIN, lysstyrke)

@socketio.on('hent_temp')
def hent_temp():
    sleep(0.5)
    socketio.emit('temp', sidste_temp)

@socketio.on('pumpstate')
def Pump(data):
    #pi.write(27, int(data))
    pi.set_PWM_dutycycle(LED_PIN, data)

@socketio.on('gather_soil_percent')
def gather_soil_percent():
    sleep(0.5)
    socketio.emit("soil", soil_percent)

@app.route("/")
def home():
    knap_tilstand = str(pi.read(BUT_PIN))
    return render_template("home.html", knap_tilstand=knap_tilstand)

@app.route("/site1/")
def site1():
    return render_template("site1.html")

@app.route("/site2/")
def site2():
    return render_template("site2.html")

@app.route("/site3/")
def site3():
    return render_template("site3.html")

def read_temp():
    global sidste_temp
    while True:
        sleep(2)
        try:
            sidste_temp = sensor.read()
        except:
            sidste_temp = None

def read_soil():
    global soil_percent
    while True:
        rd = bus.read_word_data(i2c_address, 0)
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        data = data >> 2

        procent = (690 - data) * 100 / (690 - 317)
        soil_percent = procent

        if procent < 10:
            pi.write(27, 1)
        elif procent > 60:
            pi.write(27, 0)
        else:
            pi.write(27, 0)
        sleep(1)

temp_thread = threading.Thread(target=read_temp)
temp_thread.start()

soil_thread = threading.Thread(target=read_soil)
soil_thread.start()

if __name__ == ('__main__'):
    app.run(host="0.0.0.0", debug=True)
    # socketio.run(app, host="0.0.0.0", debug=True)