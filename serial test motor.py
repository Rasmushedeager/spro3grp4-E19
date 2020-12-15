from serial import Serial 
import time
import keyboard

def send_data(m1, m2):

    b0m1 = (m1 & 0b00111111) 
    b1m1 = ((m1 >> 6) & 0b00111111) + 0b01000000

    b0m2 = (m2 & 0b00111111) + 0b10000000
    b1m2 = ((m2 >> 6) & 0b00111111) + 0b11000000

    data = [b0m1, b1m1, b0m2, b1m2]
    sent_bytes = arduino.write(data)
    print('wrote nr off bytes ' +  str(sent_bytes))

arduino = Serial('COM6', 9600, timeout=1)
print("connected")
time.sleep(1)
while True:
    m1 = input("m1(12 bit): ")
    m2 = input('m2(12 bit): ')
    send_data(int(m1), int(m2))