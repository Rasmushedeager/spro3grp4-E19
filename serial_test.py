import serial 
import time

arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
print("connected")
while True:
    time.sleep(1)
    print(arduino.readline())
