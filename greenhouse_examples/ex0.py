import pigpio
from time import sleep

BUT_PIN = 4
LED_PIN = 26

pi = pigpio.pi()
pi.set_PWM_range(LED_PIN, 100)
pi.set_PWM_dutycycle(LED_PIN, 0)
i = 0

while True:
    if pi.read(BUT_PIN) == 0:
        i = i + 5
        pi.set_PWM_dutycycle(LED_PIN, i)
        sleep(0.2)
        if i == 100:
            i = 0