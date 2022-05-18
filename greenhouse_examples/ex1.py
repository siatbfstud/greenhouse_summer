from flask import Flask
import pigpio

pi = pigpio.pi()

app = Flask(__name__)

BUT_PIN = 4

@app.route("/")
def index():
    if pi.read(BUT_PIN) == 0:
        return "Trykket"
    else:
        return "Sluppet"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)