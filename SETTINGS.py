# DEBUGGING:
DISABLE_DRIVER = False
FAKE_GPS = False
FAKE_DIR = False
LOG_DATA = False


DISTANCE_LOOK = 600 # cm
DISTANCE_THRESHOLD = 590 # cm
SPEED_DROP_OFF_DIST = 300 # cm

VEHICLE_WIDTH = 40 + (2 * 7.1)  # cm
VEHICLE_SIDE_COLLISION_OFFSET = 50 # cm
VEHICLE_FRONT_COLLISION_OFFSET = 100 # cm
VEHICLE_HIT_BOX = VEHICLE_WIDTH + VEHICLE_SIDE_COLLISION_OFFSET * 2
VEHICLE_LENGTH = 60  # cm

# VESC SETTINGS
VESC_MID = 2047
VESC_MAX = 4094
VESC_MIN = 1
DUTY_CYCLE_MODULATION = 50 # PERCENT

# the cost for deviating from the desired route
IDEAL_ROUTE_DEVIATE_COST = 5
ROUTE_COST = 0.5

# the cost for safety distance to
SAFETY_COST = 1.0

SHARP_MIN_DIST = 70  # CM
COLLISION_REVERSE_DELAY_TIME = 0.6  # The amount of time [s] to reverse after free of collision

COMPASS_ANGLE_ADJUST = -180 - 248 + 151  +20 -40
# -224 adjusted # Adjust heading to robot declination etc etc
HEADING_OFFSET_ADJUST = 0 # Set in code

NAV_PORT = "nav_port" # "COM10"
SENSOR_PORT = "sensor_port"
MOTOR_PORT = "motor_port"

# CONTROL
MAX_BIAS = 255
K_P = 1.0
Q_FACTOR = 0.7  # Determines the linearity of the control curve if < 1 Fast reaction time in the beginning,
# if > 1 slow reaction time in the beginning
SPEED_Q_FACTOR = 1.7

# Visualization offsets:
SCREEN_RESOLUTION = (1280, 720)  # (2560*(2/3), 1440*(2/3)) #(1280, 800)

V_SCALE = (SCREEN_RESOLUTION[1]*0.70) / 620  # 0-1 = 0-100%
CANVAS_SIZE = (660*V_SCALE, 620*V_SCALE)
VISUAL_X_OFFSET = 330 * V_SCALE
VISUAL_Y_OFFSET = 610 * V_SCALE
