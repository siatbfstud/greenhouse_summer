from flask import Flask, redirect
import pigpio

LED_PIN = 26

pi = pigpio.pi()

app = Flask(__name__)

@app.route("/")
def index():
    return "<a href='/on'>TÆND</a> <a href='/off'>SLUK</a>"

@app.route("/on")
def on():
    pi.write(LED_PIN, 1)
    return redirect("/")

@app.route("/off")
def off():
    pi.write(LED_PIN, 0)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)