from time import *  # Used for timing
from serial import *  # Used for serial communication with the arduino
import json  # Parsing of data from Arduino
import threading
from SETTINGS import *
from collision_avoidance_algorithm import *
from gps_functions import *
from navigation import *
import os
import signal
import sys
import board  # https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/digital-i-o
import digitalio

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT

e_stop =  digitalio.DigitalInOut(board.D17)
e_stop.direction = digitalio.Direction.INPUT

direction_data = False
location_data = False

MOTOR_PORT_INITALIZED = "..."

def get_motor_port():
    return MOTOR_PORT_INITALIZED

def get_coordinate(data_in):
    lat = getDecimal(data_in['lat'])
    lon = getDecimal(data_in['lon'])

    return lat, lon


def get_degree(data_in):
    value = data_in['dir'] + COMPASS_ANGLE_ADJUST
    return (value + 360) % 360


def get_direction():
    return direction_data


def get_location():
    return location_data


def usb_address_define():
    ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2"]

    global NAV_PORT
    global SENSOR_PORT
    global MOTOR_PORT
    
    for port in ports:
        print("Testing port: ", port)
        ser_state = False  # Connection state
        while not ser_state:  # If not connected, try again
            if not button.value:
                state_handler.shutdown_flag = True
            #os.kill(os.getpid(), signal.SIGINT)
            if state_handler.shutdown_flag:
                print("Switch turned off")
                sys.exit()
            try:  # Set up error catch
                serial_conn = Serial(port, 9600, timeout=4)  # Trying to connect serial
                serial_conn.setDTR(False)
                sleep(1)
                serial_conn.flushInput()
                serial_conn.setDTR(True)
                print("Successfully connected to ", port)  # Print for the console
                try:
                    print("Going to read data...")
                    data = serial_conn.readline()
                    print("Inital data read: ", data)
                    decoded = unicode(data, "utf-8")
                    print("Inital data decoded: ", decoded)
                    if decoded == "NAV\n":
                        print("Found the Navigation controller on port: ", port)
                        NAV_PORT = port
                        print("This is the nav port in settings: ", NAV_PORT)
                        ser_state = True  # If successful set the connection state true
                    elif decoded == "SENS\n":
                        print("Found the Sensor controller on port: ", port)
                        SENSOR_PORT = port
                        print("This is the sensor port in settings: ", SENSOR_PORT)
                        ser_state = True  # If successful set the connection state true
                    elif decoded == "MOTOR\r\n":
                        print("Found the Motor controller on port: ", port)
                        MOTOR_PORT = port
                        MOTOR_PORT_INITALIZED = port
                        state_handler.motor_port = port
                        print("This is the motor port in settings: ", MOTOR_PORT)
                        ser_state = True  # If successful set the connection state true
                    else:
                        print("Port match not found for:", data)
                except SerialException:
                    print("Nothing read")
            except SerialException:  # Error handling
                if not button.value:
                    os.kill(os.getpid(), signal.SIGINT)
                print('Trying to connect ', port)  # Inform the user that we are trying to connect
                sleep(0.5)  # Wait 0.5 second before trying again
    print("Done finding ports")


def serial_connect(port):  # This function connects the Navigation Controller
    ser_state = False  # Connection state
    while not ser_state:  # If not connected, try again
            if not button.value:
                state_handler.shutdown_flag = True
                #os.kill(os.getpid(), signal.SIGINT)
            if state_handler.shutdown_flag:
                print("Switch turned off")
                sys.exit()
            try:  # Set up error catch
                serial_conn = Serial(port, 9600, timeout=4)  # Trying to connect serial
                serial_conn.setDTR(False)
                sleep(1)
                serial_conn.flushInput()
                serial_conn.setDTR(True)
                print("Successfully connected to ", port)  # Print for the console
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
                if not button.value:
                    os.kill(os.getpid(), signal.SIGINT)
                print('Trying to connect ', port)  # Inform the user that we are trying to connect
                sleep(0.5)  # Wait 0.5 second before trying again


def decode_json_data(data):
    try:
        return json.loads(data.decode('utf-8'))
    except:
        return False


def get_navigation_data():
    ser = serial_connect(NAV_PORT)  # Define ser as the serial connection.
    ser.readline()  # Read the buffer to clear any unwanted bytes
    while True:
        if not button.value:
            state_handler.shutdown_flag = True
            #os.kill(os.getpid(), signal.SIGINT)
        if state_handler.shutdown_flag:
            sys.exit()

        state_handler.emergency_stop_flag = not e_stop.value

        try:
            data = ser.readline()  # Read the serial data from the Arduino
            if data.decode('utf-8') != '':  # If there is data
                # test = json.loads(data.decode('utf-8'))  # Decode the data from the Arduino
                test_data = decode_json_data(data)
                if test_data != False:
                    state_handler.navigation_disconnect_flag = False
                    if test_data['data'] == 0:
                        global direction_data
                        direction_data = test_data
                    if test_data['data'] == 1:  # 1 means gps data, a 0 would be the direction data
                        global location_data
                        location_data = test_data
                        # Print all the data
                else:
                    print("Data Error on navigation port, raw data: ", data)
                    # sleep(0.2)
                    # state_handler.navigation_disconnect_flag = True
            else:
                print("Timeout on Navigation - Trying again...")
                # state_handler.navigation_disconnect_flag = True
        except SerialException:
            # Disconnect of USB->UART occurred
            print("Device disconnected")
            state_handler.navigation_disconnect_flag = True
            ser = serial_connect(NAV_PORT)

def sensor_bool_convert(sensor_value):
    if sensor_value == 1:
        return True
    else:
        return False


def get_sensor_data():

    print("SENSOR LOOP STARTED")

    ser = serial_connect(SENSOR_PORT)  # Define ser as the serial connection.
    ser.flushInput()
    ser.readline()  # Read the buffer to clear any unwanted bytes
    while True:
        if not button.value:
            state_handler.shutdown_flag = True
            #os.kill(os.getpid(), signal.SIGINT)
        if state_handler.shutdown_flag:
            sys.exit()

        state_handler.emergency_stop_flag = not e_stop.value

        try:
            data = ser.readline()  # Read the serial data from the Arduino
            if data.decode('utf-8') != '':  # If there is data
                # test = json.loads(data.decode('utf-8'))  # Decode the data from the Arduino
                test_data = decode_json_data(data)
                if test_data != False:
                    state_handler.sensor_disconnect_flag = False
                    # Got the data, pass it and set different states of control system etc etc
                    
                    state_handler.front_collision_flag = sensor_bool_convert(test_data['T_F'])
                    state_handler.rear_collision_flag = sensor_bool_convert(test_data['T_B'])

                    ir_data = test_data['IR']
                    sharp_data = test_data['SHARP']

                    state_handler.ir_front_left = sensor_bool_convert(ir_data[0])
                    state_handler.ir_front_right = sensor_bool_convert(ir_data[1])
                    state_handler.ir_rear_left = sensor_bool_convert(ir_data[2])
                    state_handler.ir_rear_right = sensor_bool_convert(ir_data[3])

                    state_handler.json_string_recieved = test_data

                    state_handler.sharp_front = sharp_data[0]
                    
                    if (state_handler.motor_driver_disconnect_flag is False and state_handler.navigation_disconnect_flag
                        is False and state_handler.emergency_stop_flag is False):
                        print("Sending ACK")
                        ser.write(69)  # ACK to the sensor controller
                        print("Did send ACK")

                else:
                    print("Data Error on sensor controller, raw data: ", data)
                    state_handler.sensor_disconnect_flag = True
            else:
                print("Timeout on Sensor - Trying again...")
                state_handler.sensor_disconnect_flag = True
        except SerialException:
            # Disconnect of USB->UART occurred
            print("Device disconnected")
            state_handler.sensor_disconnect_flag = True
            ser = serial_connect(SENSOR_PORT)



nav_loop = threading.Thread(name="background", target=get_navigation_data)
sensor_loop = threading.Thread(name='background', target=get_sensor_data)

def serial_init():
    nav_loop.start()
    sensor_loop.start()
