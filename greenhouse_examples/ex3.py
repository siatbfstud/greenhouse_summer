from flask import Flask, redirect, render_template
from flask_socketio import SocketIO
import pigpio

pi = pigpio.pi()

BUT_PIN = 4

app = Flask(__name__)

socketio = SocketIO(app)

def skift(gpio, level, tick):
    socketio.emit("skift", {"tilstand": level})

pi.callback(BUT_PIN, pigpio.EITHER_EDGE, skift)

@socketio.on("connect")
def connect():
    print("Connection established")

@app.route("/")
def index():
    knap_tilstand = str(pi.read(BUT_PIN))
    return render_template("index.html", knap_tilstand=knap_tilstand)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)