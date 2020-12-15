import SETTINGS
from motor_driver import *
import time


class state_handler_class:

    def __init__(self):

        self.motor_driver = Motor_driver()

        self.shutdown_flag = False

        self.front_collision_flag = False
        self.rear_collision_flag = False
        self.emergency_stop_flag = False
        self.motor_driver_disconnect_flag = False
        self.navigation_disconnect_flag = False
        self.sensor_disconnect_flag = False

        self.motor_port = "no_init"

        self.json_string_recieved = ""

        self.sharp_front = 0
        self.sharp_rear = 0
        self.sharp_left = 0
        self.sharp_right = 0

        self.ir_front_right = 0
        self.ir_front_left = 0
        self.ir_rear_right = 0
        self.ir_rear_left = 0

        self.min_kinect_dist = 0

        self.state_string = "OPERATING NORMAL STATE"
        self.state_string_color = "#00ff00"

        # Turn directions, for multiply
        self.left = 0
        self.right = 1

    def get_base_speed_offset(self):
        speed_multiplier = (self.min_kinect_dist ** SETTINGS.SPEED_Q_FACTOR) / (
                    SETTINGS.SPEED_DROP_OFF_DIST ** SETTINGS.SPEED_Q_FACTOR)
        if speed_multiplier > 1:
            speed_multiplier = 1
        return speed_multiplier  # Return number between 0 and 1 depending on how close we are to any given object. from kinect

    # If no clear routes, turn a bit and return

    def look_for_clear_routes(self, desired_heading):
        if desired_heading > 0:
            self.motor_driver.set_motor_speed(0, 25)
        else:
            self.motor_driver.set_motor_speed(25, 0)

    # Manage hard collisions:

    def stop_motors(self):
        self.motor_driver.set_motor_speed(0, 0)

    def hard_collision_manager(self):
        print("Now handling collisions")

        # Find direction to turn:
        direction_decider = 0
        if self.ir_front_left:
            direction_decider += 1

        if self.ir_front_right:
            direction_decider -= 1

        while self.front_collision_flag:
            if self.rear_collision_flag:
                print("Unable to move")
                self.motor_driver.set_motor_speed(0, 0)
                return
            else:
                print("Going backwards now...")
                self.motor_driver.set_motor_speed(-25, -25)
                print("Did send command!")
        time.sleep(SETTINGS.COLLISION_REVERSE_DELAY_TIME)
        self.motor_driver.set_motor_speed(0, 0)
        time.sleep(SETTINGS.COLLISION_REVERSE_DELAY_TIME)

        if direction_decider <= 0:  # Right blocked, thus drive left
            self.motor_driver.set_motor_speed(0, 25)

        else:  # Left blocked, drive right
            self.motor_driver.set_motor_speed(25, 0)
        
        time.sleep(SETTINGS.COLLISION_REVERSE_DELAY_TIME * 2)

        self.motor_driver.set_motor_speed(25, 25)

        time.sleep(SETTINGS.COLLISION_REVERSE_DELAY_TIME * 2)

        self.motor_driver.set_motor_speed(0, 0)

        return True


state_handler = state_handler_class()
