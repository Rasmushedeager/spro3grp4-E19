import tkinter as tk
from math import *
from SETTINGS import *
from navigation import state_handler

master = tk.Tk()
gui = tk.Canvas(master, width=SCREEN_RESOLUTION[0], height=SCREEN_RESOLUTION[1])
w = tk.Canvas(None, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
data_view = tk.Canvas(None, width=SCREEN_RESOLUTION[0] * 0.5 - 30, height=SCREEN_RESOLUTION[1] * 0.8 - 30)
state_view = tk.Canvas(None, width=SCREEN_RESOLUTION[0] * 0.5 - 10, height=SCREEN_RESOLUTION[1] * 0.1)
# w.pack()

master.config(cursor='none')
master.attributes("-fullscreen", True)

gui.pack()


def init_gui():
    gui.create_rectangle(0, 0, SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1] * 0.1, fill="white", outline="white")
    gui.create_rectangle(0, SCREEN_RESOLUTION[1] * 0.9, SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1] * 1, fill="white",
                         outline="white")
    gui.create_line(SCREEN_RESOLUTION[0] * 0.5, 0, SCREEN_RESOLUTION[0] * 0.5, SCREEN_RESOLUTION[1], fill="black",
                    width=5)
    gui.create_text(SCREEN_RESOLUTION[0] * 0.25, SCREEN_RESOLUTION[1] * 0.05, fill="black", font="Arial 25",
                    text="Visualization", anchor=tk.CENTER, justify=tk.CENTER)
    gui.create_text(SCREEN_RESOLUTION[0] * 0.75, SCREEN_RESOLUTION[1] * 0.05, fill="black", font="Arial 25",
                    text="Data", anchor=tk.CENTER, justify=tk.CENTER)
    gui.create_text(20, SCREEN_RESOLUTION[1] * 0.95, fill="black", font="Arial 25",
                    text="Status:", anchor=tk.W, justify=tk.LEFT)

    gui.create_window(SCREEN_RESOLUTION[0] * 0.25, SCREEN_RESOLUTION[1] * 0.5, anchor=tk.CENTER, window=w)
    gui.create_window(SCREEN_RESOLUTION[0] * 0.75, SCREEN_RESOLUTION[1] * 0.5, anchor=tk.CENTER, window=data_view)
    gui.create_window(SCREEN_RESOLUTION[0] * 0.25, SCREEN_RESOLUTION[1] * 0.95, anchor=tk.CENTER, window=state_view)


def init_canvas():
    w.delete('all')
    data_view.delete('all')
    state_view.delete('all')


def create_sweep(data):
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET - data[0] * V_SCALE,
                  VISUAL_Y_OFFSET - data[1] * V_SCALE, fill="green", width=3 * V_SCALE)
    w.create_line(VISUAL_X_OFFSET - data[0] * V_SCALE, VISUAL_Y_OFFSET - data[1] * V_SCALE,
                  VISUAL_X_OFFSET - data[2] * V_SCALE, VISUAL_Y_OFFSET - data[3] * V_SCALE, fill="red",
                  width=3 * V_SCALE)


def insert_kinect_image_with_filter():
    pass
    # img = ImageTk.PhotoImage(Image.open("image.png"))
    # w.create_image(100,100, image=img)


def create_current_heading():
    v_W = VEHICLE_WIDTH * V_SCALE
    v_L = VEHICLE_LENGTH * V_SCALE
    v_H = VEHICLE_HIT_BOX * V_SCALE

    x_off = 7.1 * V_SCALE
    y_off = 8.5 * V_SCALE
    wheel_dia = 17 * V_SCALE
    wheel_w = 5 * V_SCALE

    w.create_rectangle(VISUAL_X_OFFSET - v_W / 2 + x_off, VISUAL_Y_OFFSET + y_off, VISUAL_X_OFFSET + v_W / 2 - x_off,
                       VISUAL_Y_OFFSET + y_off - v_L, fill="blue", outline='blue')
    w.create_rectangle(VISUAL_X_OFFSET - v_W / 2 + x_off, VISUAL_Y_OFFSET + y_off,
                       VISUAL_X_OFFSET - v_W / 2 + x_off - wheel_w, VISUAL_Y_OFFSET + y_off - wheel_dia, fill="black",
                       outline='black')
    w.create_rectangle(VISUAL_X_OFFSET + v_W / 2 - x_off, VISUAL_Y_OFFSET + y_off,
                       VISUAL_X_OFFSET + v_W / 2 - x_off + wheel_w, VISUAL_Y_OFFSET + y_off - wheel_dia, fill="black",
                       outline='black')
    w.create_rectangle(VISUAL_X_OFFSET - v_H / 2 + x_off, VISUAL_Y_OFFSET + y_off, VISUAL_X_OFFSET + v_H / 2 - x_off,
                       VISUAL_Y_OFFSET + y_off - v_L - VEHICLE_FRONT_COLLISION_OFFSET * V_SCALE, outline='red')
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET, 5, fill="blue", width=3,
                  arrow=tk.LAST)  # Current heading


def create_text(heading, posistion, target, dist_to_target, heading_offset, speed_parameters, route_offset, fps, json, running):
    heading_string = "Compass heading:\nOffset to desired direction:\nOffset to best route:\nCurrent coords:\nTarget coords:\nDistance to target:\nBase speed:"
    data_string = ("{}°\n{}°\n{}°\n({}, {})\n({}, {})\n{}m\n{}%\n{}\n{}").format(
        format(heading, ".1f"), format(heading_offset, ".1f"), format(route_offset, ".1f"), format(posistion[0], ".6f"), format(posistion[1], ".6f"),
        target[0], target[1], dist_to_target, format(speed_parameters[0], ".2f"), json, running)

    data_view.create_text(0, 0, fill="black", font="Arial 17",
                          text=heading_string, anchor=tk.NW, justify=tk.LEFT)
    data_view.create_text(SCREEN_RESOLUTION[0] * 0.5 - 30, 0, fill="black", font="Arial 17",
                          text=data_string, anchor=tk.NE, justify=tk.RIGHT)
    m1_string = ("{}%").format(format(speed_parameters[1], ".0f"))
    m2_string = ("{}%").format(format(speed_parameters[2], ".0f"))

    v_W = VEHICLE_WIDTH * V_SCALE
    v_L = VEHICLE_LENGTH * V_SCALE
    v_H = VEHICLE_HIT_BOX * V_SCALE

    x_off = 7.1 * V_SCALE
    y_off = 8.5 * V_SCALE
    wheel_dia = 17 * V_SCALE
    wheel_w = 5 * V_SCALE
    fps_string = "FPS: {}".format(format(fps, ".2f"))
    w.create_text(VISUAL_X_OFFSET - v_H / 2 - wheel_w, VISUAL_Y_OFFSET - wheel_dia / 2, fill="black", font="Arial 10",
                  text=m1_string, anchor=tk.NE, justify=tk.RIGHT)
    w.create_text(VISUAL_X_OFFSET + v_H / 2 + wheel_w, VISUAL_Y_OFFSET - wheel_dia / 2, fill="black", font="Arial 10",
                  text=m2_string, anchor=tk.NW, justify=tk.LEFT)
    w.create_text(12, VISUAL_Y_OFFSET - 15, fill="black", font="Arial 15",
                  text=fps_string, anchor=tk.NW, justify=tk.LEFT)


def update_master():

    state_view.create_rectangle(0, 0, SCREEN_RESOLUTION[0] * 0.5, SCREEN_RESOLUTION[1] * 0.1, fill="white", outline="white")
    state_view.create_text(30, SCREEN_RESOLUTION[1] * 0.05, fill=state_handler.state_string_color, font="Arial-Black 25",
                    text=state_handler.state_string, anchor=tk.W, justify=tk.LEFT)

    w.update()
    gui.update()
    master.update()


def create_span_gap(angle_in, dist, text):
    angle = -angle_in + 61.5 + 28.5
    x_coor = (cos(angle * pi / 180) * dist * V_SCALE)
    y_coor = (sin(angle * pi / 180) * dist * V_SCALE)
    if text > VEHICLE_HIT_BOX:
        w.create_text(VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="black", font="Arial 10",
                      text=format(text, ".2f"))
    else:
        w.create_text(VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="red", font="Arial 10",
                      text=format(text, ".2f"))


def create_angle_line(angle_in):
    angle = -angle_in + 61.5 + 28.5
    x_coor = (cos(angle * pi / 180) * 600 / sin(radians(angle)) * V_SCALE)
    y_coor = (sin(angle * pi / 180) * 600 / sin(radians(angle)) * V_SCALE)
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="black",
                  width=1)  # Heading
    w.create_text(VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="black", font="Arial 10",
                  text=format(angle_in, ".2f"))


def create_desired_heading_line(angle_in):
    angle = -angle_in + 61.5 + 28.5
    x_coor = (cos(angle * pi / 180) * 600 * V_SCALE)
    y_coor = (sin(angle * pi / 180) * 600 * V_SCALE)
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="purple",
                  width=4, arrow=tk.LAST)  # Heading


def create_best_possible_heading_line(angle_in):
    print(angle_in)
    angle = -angle_in + 61.5 + 28.5
    x_coor = (cos(angle * pi / 180) * 620 * V_SCALE)
    y_coor = (sin(angle * pi / 180) * 620 * V_SCALE)
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="black",
                  width=2, arrow=tk.LAST)  # Heading


def create_possible_route_line(angle_in):
    angle = angle_in
    x_coor = (cos(angle * pi / 180) * 550 * V_SCALE)
    y_coor = (sin(angle * pi / 180) * 550 * V_SCALE)
    w.create_line(VISUAL_X_OFFSET, VISUAL_Y_OFFSET, VISUAL_X_OFFSET - x_coor, VISUAL_Y_OFFSET - y_coor, fill="yellow",
                  width=2, arrow=tk.LAST)  # Heading


def draw_point(x, y):
    x1 = VISUAL_X_OFFSET - x * V_SCALE
    y1 = VISUAL_Y_OFFSET - y * V_SCALE
    # print("Point: (", x1, ", ", y1, ")")
    w.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="yellow")
