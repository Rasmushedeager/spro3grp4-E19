import board  # https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/digital-i-o
import digitalio
import time

e_stop =  digitalio.DigitalInOut(board.D17)
e_stop.direction = digitalio.Direction.INPUT

while True:
    print(e_stop.value)
    time.sleep(0.2)