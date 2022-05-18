import pigpio, threading, smbus
from flask import Flask, redirect, render_template
from flask_socketio import SocketIO, emit
from time import sleep

RED_LED_PIN = 20
BLUE_LED_PIN = 21
PUMP_PIN = 23

soil_percent = None

app = Flask(__name__)
pi = pigpio.pi()

#Til LED
pi.set_PWM_range(RED_LED_PIN, 100)
pi.set_PWM_range(BLUE_LED_PIN, 100)
pi.set_PWM_frequency(RED_LED_PIN, 100000)
pi.set_PWM_frequency(BLUE_LED_PIN, 100000)

#Til Jordmåler
pi.set_mode(PUMP_PIN, pigpio.OUTPUT)
bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x49# default address

socketio = SocketIO(app)

@socketio.on('blue_led_state')
def blue_led_func(data):
    pi.set_PWM_dutycycle(BLUE_LED_PIN, data)

@socketio.on('red_led_state')
def red_led_func(data):
    pi.set_PWM_dutycycle(RED_LED_PIN, data)

@socketio.on('pumpstate')
def Pump(data):
    pi.write(PUMP_PIN, int(data))

@socketio.on('gather_soil_percent')
def gather_soil_percent():
    sleep(0.5)
    socketio.emit("soil", soil_percent)

@app.route("/")
def index():
    return render_template("index.html")

def read_soil():
    global soil_percent
    while True:
        rd = bus.read_word_data(i2c_address, 0)
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        data = data >> 2
        print(data)

        procent = (470 - data) * 100 / (470 - 217)
        
        if procent < 0:
            procent = 0.0
        if procent > 100:
            procent = 100

        soil_percent = procent

        if procent < 10:
            pi.write(PUMP_PIN, 1)
        elif procent > 60:
            pi.write(PUMP_PIN, 0)
        else:
            pi.write(PUMP_PIN, 0)
        sleep(1)


soil_thread = threading.Thread(target=read_soil)
soil_thread.start()

if __name__ == ('__main__'):
    app.run(host="0.0.0.0", debug=True)