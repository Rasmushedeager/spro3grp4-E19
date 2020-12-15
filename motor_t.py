from time import *  # Used for timing
from serial import *  # Used for serial communication with the arduino
import json  # Parsing of data from Arduino
#import threading
from SETTINGS import *
#from gps_functions import *
#from navigation import *



class Motor_driver:

    def __init__(self):
        global MOTOR_ERROR_FLAG
        self.driver = self.motor_diver_connect()
        self.m1_last = 0
        self.m2_last = 0

    def motor_diver_connect(self):
        ser_state = False  # Connection state
        times_tried = 0
        while not ser_state:  # If not connected, try again
            if times_tried < 10:
                times_tried += 1
                try:  # Set up error catch
                    serial_conn = Serial("/dev/ttyUSB1", 9600, timeout=4)  # Trying to connect serial
                    serial_conn.setDTR(False)
                    sleep(1)
                    serial_conn.flushInput()
                    serial_conn.setDTR(True)
                    print("Successfully connected to motor")  # Print for the console
                    try:
                        print("Going to read data...")
                        data = serial_conn.readline()
                        print("Inital data read: ", data)
                        decoded = unicode(data, "utf-8")
                        print("Inital data decoded: ", decoded)
                        ser_state = True
                    except SerialException:
                        print("Nothing read")
                    return serial_conn

                except SerialException:  # Error handling
                    print('Trying to connect motor')  # Inform the user that we are trying to connect
                    sleep(0.5)  # Wait 0.5 second before trying again
            else:
                return False

    def set_motor_speed(self, motor1_speed, motor2_speed):
        global MOTOR_ERROR_FLAG

        if motor1_speed > DUTY_CYCLE_MODULATION:
            motor1_speed = DUTY_CYCLE_MODULATION
        
        if motor2_speed > DUTY_CYCLE_MODULATION:
            motor2_speed = DUTY_CYCLE_MODULATION

        if self.driver is not False:
            try:

                print("Got this far!")

                m1 = VESC_MID + ((motor1_speed / 100.0) * (VESC_MAX - VESC_MID - 10))
                m2 = VESC_MID + ((motor2_speed / 100.0) * (VESC_MAX - VESC_MID - 10))

                if m1 > VESC_MAX:
                    m1 = VESC_MAX
                elif m1 < VESC_MIN:
                    m1 = VESC_MIN

                if m2 > VESC_MAX:
                    m2 = VESC_MAX
                elif m2 < VESC_MIN:
                    m2 = VESC_MIN

                m1 = int(m1)
                m2 = int(m2)

                b0m1 = (m1 & 0b00111111)
                b1m1 = ((m1 >> 6) & 0b00111111) + 0b01000000

                b0m2 = (m2 & 0b00111111) + 0b10000000
                b1m2 = ((m2 >> 6) & 0b00111111) + 0b11000000
                print("Got so far!")
                data = [b0m1, b1m1, b0m2, b1m2]
                self.driver.write(data)
                try:
                    text = self.driver.readline()
                    if len(text) != 0:
                        print("Result: ", text)
                    else:
                        print("No motor return")
                        return False
                except:
                    print("Could not read line")
                    return False
                return True
            except:
                print("Could not send data")
                return False
        else:
            print("Motor driver is false")
            return False


driver = Motor_driver()


while True:
    print("Sending command:")
    driver.set_motor_speed(0, 0)
    sleep(1)