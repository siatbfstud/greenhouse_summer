import smbus
import time
import pigpio

pi = pigpio.pi()
pi.set_mode(27, pigpio.OUTPUT)

bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x49# default address
while True:
    # Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    data = data >> 2

    procent = (690 - data) * 100 / (690 - 317)
    print(procent)
    if procent < 10:
        pi.write(27, 1)
    elif procent > 60:
        pi.write(27, 0)
    else:
        pi.write(27, 0)
    time.sleep(1)