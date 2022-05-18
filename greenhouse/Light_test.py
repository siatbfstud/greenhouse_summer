import schedule, pigpio, time

class LightScheduler:
    def __init__(self, start_time, stop_time, GPIO_pin):
        self.start_time = start_time
        self.stop_time = stop_time
        self.duty = None
        self.GPIO_pin = GPIO_pin
        # lamp is connected to GPIO pin.
        self.pi = pigpio.pi()
        self.pi.set_PWM_range(self.GPIO_pin, 100)
        
    def init_schedule(self):
        # set the schedule         
        schedule.every().day.at(self.start_time).do(self.on)         
        schedule.every().day.at(self.stop_time).do(self.off)
    
    def on(self):
        self.pi.set_PWM_dutycycle(self.GPIO_pin, 50)
    
    def off(self):
        self.pi.set_PWM_dutycycle(self.GPIO_pin, 0)
        
if __name__ == "__main__":
    lamp = LightScheduler("11:30", "11:35", 13)
    lamp.init_schedule()
    while True:
        schedule.run_pending()
        time.sleep(1)
