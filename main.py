# Navigation software, MCU MAIN THREAD - SDU GROUP 4 - 3RD SEMESTER MECHATRONICS 2020

# This software uses WGS84 Decimal Coordinates for navigation
from navigation import *
from SETTINGS import *
import sys
import kinect
kinect.init_kinect()

targetLocation = (54.914139, 9.777001)  # The location that we want to go



data = []

for x in range(690):
    if x < 73:
        data.append(460)
    elif x < 300:
        data.append(600)
    elif x < 400:
        data.append(580)
    elif x < 577:
        data.append(600)
    elif x < 600:
        data.append(230)
    elif x < 605:
        data.append(600)
    elif x < 690:
        data.append(600)

serial_init()
init_gui()

should_run = True

while should_run:

    if not button.value:
        state_handler.shutdown_flag = True
        #os.kill(os.getpid(), signal.SIGINT)
    if state_handler.shutdown_flag:
        print("Switch turned off")
        master.destroy()
        should_run = False

    nav_data = get_location()
    dir_data = get_direction()
    if len(kinect.depth_data) != 0:
        data = kinect.get_kinect_processed_data(kinect.depth_data)
    if (nav_data is not False or FAKE_GPS) and (dir_data is not False or FAKE_DIR):
        if FAKE_GPS:
            currentLocation = (54.912192, 9.780407)  # CHEATING TO TEST E-COMPASS
        else:
            currentLocation = get_coordinate(nav_data)

        if FAKE_DIR:
            direction = 55
        else:
            direction = get_degree(dir_data)

        if currentLocation[0] != 0:
            run_calculations(data, direction, currentLocation, targetLocation)
        else:
            print("Waiting for GPS signal...")
            sleep(5)

        # Note getDecimal, this function converts the minute, part of the data to degrees decimal.

print("Program stopped by button, to start: Flip the switch again!")