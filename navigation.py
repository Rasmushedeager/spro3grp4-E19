from SETTINGS import *
from collision_avoidance_algorithm import *
from serial_cummunications import *
from visualization import *
import time
import datetime

state = 0

did_have_e_stop_condition = False

# Set up data logging:
now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
log_name = "logfile_{}.txt".format(dt_string)
if LOG_DATA:
    print("FILENAME FOR LOG:", log_name)
    file = open(log_name, "w+")
    file.write("{}\r\n".format(log_name))
    file.close()

prev_time = int(round(time.time() * 1000))

usb_address_define()

print("Initializing motor driver for later use..")

if state_handler.motor_driver.driver is False:
    print("\n\n\nConnecting to motor driver!")
    state_handler.motor_driver.driver = state_handler.motor_driver.motor_diver_connect(state_handler.motor_port)

if state_handler.motor_driver.driver is False:
    print("Motor driver not connected...")
    state_handler.motor_driver_disconnect_flag = True
else:
    sleep(2)
    state_handler.motor_driver_disconnect_flag = False
    print("Its initialized with a 2 second delay after to wake up the arduino")

def set_emergency_state(state):
    state_handler.emergency_stop_flag = state

def get_clear_routes(ob_points):
    possible_routes = []
    clear_path_points = []
    indexes = []
    for x in range(len(ob_points)):
        if ob_points[x][3] > DISTANCE_THRESHOLD:
            clear_path_points.append(ob_points[x])
            indexes.append(x)

    count = len(clear_path_points)

    start_index = 0

    for x in range(count):
        if x + 1 != count:
            if clear_path_points[x][4] + 1 != clear_path_points[x + 1][4]:
                # print("First_angle: ", clear_path_points[start_index][2], " Second Angle: ", clear_path_points[x][2])
                create_angle_line(clear_path_points[start_index][2])
                create_angle_line(clear_path_points[x][2])
                possible_angle = (clear_path_points[start_index][2] + clear_path_points[x][2]) / 2
                # create_possible_route_line(possible_angle)

                possible_routes.append((
                    clear_path_points[start_index][2], indexes[start_index], clear_path_points[x][2],
                    indexes[x]))  # (first_angle, index1, second_angle, index2)

                start_index = x + 1
        else:
            # print("First_angle: ", clear_path_points[start_index][2], " Second Angle: ", clear_path_points[x][2])
            create_angle_line(clear_path_points[start_index][2])
            create_angle_line(clear_path_points[x][2])
            possible_angle = (clear_path_points[start_index][2] + clear_path_points[x][2]) / 2
            # create_possible_route_line(possible_angle)
            possible_routes.append(
                (clear_path_points[start_index][2], indexes[start_index], clear_path_points[x][2], indexes[x]))
            start_index = x + 1

    return possible_routes


def get_best_route(data, free_angles, desired_route_offset):
    possible_routes = []
    for span in free_angles:
        angle1 = -(span[0]) + 61.5 + 28.5
        angle2 = -(span[2]) + 61.5 + 28.5
        l1 = 0
        l2 = 0
        closest_dist_border = (VEHICLE_HIT_BOX / 2)
        if span[1] - 1 >= 0:
            l1 = data[span[1] - 1] / sin(radians(angle1))
            if l1 <= closest_dist_border:
                # print("l1 less than 0: ", l1, "index: ", span[1] - 1, " set to ", closest_dist_border)
                l1 = closest_dist_border
                # pass
        else:
            l1 = 600 / sin(radians(angle1))
        if span[3] + 1 < len(data):
            l2 = data[span[3] + 1] / sin(radians(angle2))
            if l2 <= closest_dist_border:
                # print("l2 less than 0: ", l2, "index: ", span[3] + 1, " set to ", closest_dist_border)
                l2 = closest_dist_border
                # pass
        else:
            l2 = 600 / sin(radians(angle2))

        angle_gap = span[0] - span[2]
        min_dist = 0
        max_dist = 0
        short_side = 0
        if l1 > l2:
            min_dist = l2
            max_dist = l1
            short_side = 1
        else:
            min_dist = l1
            max_dist = l2

        small_span = 2 * sin((angle_gap / 2) * pi / 180) * min_dist
        large_span = 2 * sin((angle_gap / 2) * pi / 180) * max_dist

        create_span_gap(span[0] - 5, min_dist, small_span)
        create_span_gap(span[0] - 5, max_dist, large_span)

        x_p1 = (cos(angle1 * pi / 180) * min_dist)
        y_p1 = (sin(angle1 * pi / 180) * min_dist)
        draw_point(x_p1, y_p1)
        x_p2 = (cos(angle2 * pi / 180) * min_dist)
        y_p2 = (sin(angle2 * pi / 180) * min_dist)
        draw_point(x_p2, y_p2)

        x_p1 = (cos(angle1 * pi / 180) * max_dist)
        y_p1 = (sin(angle1 * pi / 180) * max_dist)
        draw_point(x_p1, y_p1)
        x_p2 = (cos(angle2 * pi / 180) * max_dist)
        y_p2 = (sin(angle2 * pi / 180) * max_dist)
        draw_point(x_p2, y_p2)

        if small_span > VEHICLE_HIT_BOX:
            angle_in = angle2 - angle_gap / 2
            new_offset_angle = -angle_in + 61.5 + 28.5

            offset_from_main = new_offset_angle - desired_route_offset
            closest_angle_offset = asin((VEHICLE_HIT_BOX / 2) / min_dist) * 180 / pi
            furthest_angle_offset = asin((VEHICLE_HIT_BOX / 2) / max_dist) * 180 / pi
            first_angle_max_offset = 0
            second_angle_max_offset = 0
            if short_side == 0:

                first_angle_max_offset = angle1 + closest_angle_offset
                second_angle_max_offset = angle2 - furthest_angle_offset
            else:
                first_angle_max_offset = angle1 + furthest_angle_offset
                second_angle_max_offset = angle2 - closest_angle_offset

            # print("First and second angle max offset: ", first_angle_max_offset, ", ", second_angle_max_offset)
            create_possible_route_line(first_angle_max_offset)
            create_possible_route_line(second_angle_max_offset)

            first_angle_max_offset_fixed = -first_angle_max_offset + 61.5 + 28.5
            second_angle_max_offset_fixed = -second_angle_max_offset + 61.5 + 28.5
            if desired_route_offset < first_angle_max_offset_fixed and desired_route_offset > second_angle_max_offset_fixed:
                # print("Use heading offset.")
                possible_routes.append([desired_route_offset, 0, min_dist])
            elif desired_route_offset > first_angle_max_offset_fixed:
                # print("Use first angle max offset: ", first_angle_max_offset_fixed)
                possible_routes.append([first_angle_max_offset_fixed, 0, min_dist])
            elif desired_route_offset < second_angle_max_offset_fixed:
                # print("Use second angle max offset: ", second_angle_max_offset_fixed)
                possible_routes.append([second_angle_max_offset_fixed, 0, min_dist])

            # possible_routes.append([new_offset_angle, 0])
        elif large_span > VEHICLE_HIT_BOX:
            # print(min_dist)
            # print((VEHICLE_HIT_BOX / 2) / min_dist)
            closest_angle_offset = asin((VEHICLE_HIT_BOX / 2) / min_dist) * 180 / pi

            angle_in = 0
            if short_side == 0:
                angle_in = angle1 + closest_angle_offset
            else:
                angle_in = angle2 - closest_angle_offset
            new_offset_angle = -angle_in + 61.5 + 28.5
            # print(new_offset_angle)
            create_possible_route_line(angle_in)
            possible_routes.append([new_offset_angle, IDEAL_ROUTE_DEVIATE_COST, 600])

    for i in range(len(possible_routes)):
        deviation = possible_routes[i][0] - desired_route_offset
        deviation_cost = abs(deviation) * ROUTE_COST
        possible_routes[i][1] = possible_routes[i][1] + deviation_cost

    possible_routes = sorted(possible_routes, key=lambda x: x[1], reverse=False)

    # print("Desired route offset: ", possible_routes[0][0], " From: ", possible_routes)
    if len(possible_routes) == 0:
        return False
    else:
        return possible_routes[0][0]


def get_heading_offset(current_heading, current_pos, target_pos):
    target_dir = calculate_initial_compass_bearing(current_pos, target_pos)

    delta_offset = current_heading - target_dir + HEADING_OFFSET_ADJUST

    offset = (delta_offset + 360) % 360

    # print(target_dir)
    if offset > 180:  # Convert to offset from main heading
        offset = -(360 - offset)

    return offset


def p_control(heading_offset):
    bias_speed = 25 #* state_handler.get_base_speed_offset()
    bias = ((abs(heading_offset) ** Q_FACTOR) / (180 ** Q_FACTOR)) * bias_speed
    if heading_offset < 0:
        speed1 = int(bias_speed)
        speed2 = int(bias_speed - bias)
        if state_handler.motor_driver.set_motor_speed(speed1, speed2) is False:
            #state_handler.motor_driver_disconnect_flag = True
            pass
        else:
            state_handler.motor_driver_disconnect_flag = False
        return bias_speed, speed1, speed2
    else:
        speed1 = int(bias_speed - bias)
        speed2 = int(bias_speed)
        if state_handler.motor_driver.set_motor_speed(speed1, speed2) is False:
            #state_handler.motor_driver_disconnect_flag = True
            pass
        else:
            state_handler.motor_driver_disconnect_flag = False
        return bias_speed, speed1, speed2

def print_states():
    print("Front collision: ", state_handler.front_collision_flag)
    print("Emergency stop: ", state_handler.emergency_stop_flag)
    print("sensor disconnect: ", state_handler.sensor_disconnect_flag)
    print("Navigation disconnect: ", state_handler.navigation_disconnect_flag)
    print("Motor disconnect: ", state_handler.motor_driver_disconnect_flag)

def run_calculations(data_in, heading, position, target):

    init_canvas()
    runner = "nothing"
    global prev_time
    global didSetOffset
    global state
    global did_have_e_stop_condition
    minimum_distance = DISTANCE_LOOK
    data_converted = []
    ob_points = []
    heading_offset = 0
    dist_to_target = 0
    speed_parameters = 0, 0, 0
    best_route = 0
    fps = 0
    print_states()

    heading_offset = get_heading_offset(heading, position, target)
    dist_to_target = get_dist_to_target(position, target) * 1000  # Distance in meters
    for x in range(len(data_in)):
        angle = (57 / len(data_in)) * x + 61.5
        angle2 = -(57 / len(data_in)) * x + 28.5

        length = int(data_in[x])
        if length > 600:
            length = 600

        data_converted.append(length)

        if length < minimum_distance:
            minimum_distance = length

        # print("Angle: ", angle, " Length old: ", length, " Length new: ", length/sin(radians(angle)))
        length = length / sin(radians(angle))

        x_coordinate = (cos(angle * pi / 180) * length)
        y_coordinate = (sin(angle * pi / 180) * length)

        x_end_coordinate = (cos(angle * pi / 180) * 600 / sin(radians(angle)))
        y_end_coordinate = (sin(angle * pi / 180) * 600 / sin(radians(angle)))

        x_coordinate_2 = (cos(angle2 * pi / 180) * length)
        y_coordinate_2 = (sin(angle2 * pi / 180) * length)

        ob_point = [x_coordinate_2, y_coordinate_2, angle2, length, x]
        ob_points.append(ob_point)
        create_sweep((x_coordinate, y_coordinate, x_end_coordinate, y_end_coordinate))
        # print(data_converted)

    state_handler_class.min_kinect_dist = minimum_distance  # Setting the parameter for collision avoidance

    clear_routes = get_clear_routes(ob_points)

    best_route = get_best_route(data_converted, clear_routes, heading_offset)

    create_best_possible_heading_line(best_route)

    create_desired_heading_line(heading_offset)

    if not (state_handler.front_collision_flag or state_handler.emergency_stop_flag or state_handler.sensor_disconnect_flag
        or state_handler.navigation_disconnect_flag or state_handler.motor_driver_disconnect_flag):
        state_handler.state_string = "OPERATING NORMAL STATE"
        state_handler.state_string_color = "#00ff00"

        if did_have_e_stop_condition:
            state_handler.state_string = "RECONNECTING MOTORS"
            state_handler.state_string_color = "#0000ff"
            state_handler.motor_driver.driver.__del__()
            update_master()
            state_handler.motor_driver.driver = state_handler.motor_driver.motor_diver_connect(state_handler.motor_port)
            state_handler.motor_driver.set_motor_speed(0, 0)
            sleep(1)
            did_have_e_stop_condition = False

        if dist_to_target > 10:
            if best_route is False:
                runner = "Kinect has no clear route,\nturning till one is found."
                state_handler.look_for_clear_routes(heading_offset)
            else:
                runner = "Driving via P-Control"
                speed_parameters = p_control(best_route)
        else:
            runner = "Target reached! \nCongrats, the thing worked!!!"
            state_handler.motor_driver.set_motor_speed(0, 0)

    else:
        runner = "Unknown Error"
        state_handler.stop_motors()
        print("There is a condition")
        if state_handler.front_collision_flag and state_handler.rear_collision_flag is False:
            runner = "Sensor has detected an object,\ntrying to avoid"
            print("HARD COLLISION - RUNNING ALGORITHM TO AVOID")
            state_handler.state_string = "FRONT SENSOR GROUP TIGGER"
            state_handler.state_string_color = "#0000ff"
            update_master()
            if not state_handler.hard_collision_manager():
                runner = "Both sensor groups are triggered.\nThere will be no movement!"
                state_handler.state_string = "F/B TRIG - NOT MOVING"
                state_handler.state_string_color = "#ff0000"
        elif state_handler.rear_collision_flag:
            runner = "Both sensor groups are triggered.\nThere will be no movement!"
            state_handler.state_string = "F/B TRIG - NOT MOVING"
            state_handler.state_string_color = "#ff0000"
            state_handler.stop_motors()
        elif state_handler.emergency_stop_flag:
            runner = "Not running due to emergency stop"
            print("Emergency stop condition")
            state_handler.state_string = "EMERGENCY STOP CONDITION"
            state_handler.state_string_color = "#ff0000"
            did_have_e_stop_condition = True
        else:
            if state_handler.sensor_disconnect_flag:
                runner = "Not running due to\nsensor disconnect"
                state_handler.state_string = "SENSORS DISCONNECTED"
            if state_handler.motor_driver_disconnect_flag:
                runner = "Not running due to\nmotor disconnect"
                print("MOTOR DISCONNECTED FFS")
                state_handler.state_string = "MOTOR DRIVER DISCONNECTED"
            if state_handler.navigation_disconnect_flag:
                runner = "Not running due to\nnavigation disconnect"
                state_handler.state_string = "NAVIGATION DISCONNECTED"
            state_handler.state_string_color = "#ff0000"

    create_current_heading()

    new_time = int(round(time.time() * 1000))
    fps = 1000 / (new_time - prev_time)
    prev_time = new_time

    create_text(heading, position, target, dist_to_target, heading_offset, speed_parameters, best_route, fps, state_handler.json_string_recieved, runner)
    if LOG_DATA:
        data_string = "Front coll: {}\tRear coll: {}\tEmergency stop: {}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
            state_handler.front_collision_flag, state_handler.rear_collision_flag, state_handler.emergency_stop_flag,
            format(heading, ".1f"), format(heading_offset, ".1f"), format(best_route, ".1f"), position[0], position[1],
            target[0], target[1], dist_to_target, speed_parameters[0])
        log_file = open(log_name, "a+")
        log_file.write("{}\n".format(data_string))
        log_file.close()
    insert_kinect_image_with_filter()

    update_master()
