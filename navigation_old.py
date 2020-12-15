import tkinter as tk
from math import *

master = tk.Tk()

length = 600 #cm

w = tk.Canvas(master, width=620, height=620)
w.pack()



def runVisual(data_in):
    w.delete('all')
    w.create_line(310, 610, 310, 10, fill="blue", width=4)  # Heading
    ob_points = []
    for x in range(len(data_in)):

        angle = (57/len(data_in)) * x + 61.5

        length = int(data_in[x])/5

        if length > 600:
            length = 600

        x_coor = (cos(angle * pi / 180) * length)
        y_coor = (sin(angle * pi / 180) * length)

        x_end_coor = (cos(angle * pi / 180) * 600)
        y_end_coor = (sin(angle * pi / 180) * 600)

        angle2 = -(57/len(data_in)) * x + 28.5
        x_coor2 = (cos(angle2 * pi / 180) * length)
        y_coor2 = (sin(angle2 * pi / 180) * length)

        ob_point = [x_coor2, y_coor2, angle2, length, x]
        ob_points.append(ob_point)

        w.create_line(310, 610, 310 - x_coor, 610 - y_coor, fill="green", width=1.5)
        w.create_line(310 - x_coor, 610 - y_coor, 310 - x_end_coor, 610 - y_end_coor, fill="red", width=1.5)
    find_best_route(ob_points)
    master.update()


# .create_line(310, 610, 300, 100, fill="yellow", width=4, arrow=tk.LAST)  # Target direction
# w.create_line(310, 610, 380, 100, fill="blue", width=4, arrow=tk.LAST)  # Avoidance direction

def create_angle_line(angle_in):
    angle = -(angle_in) + 61.5+28.5
    x_coor = (cos(angle * pi / 180) * 600)
    y_coor = (sin(angle * pi / 180) * 600)
    w.create_line(310, 610, 310 - x_coor, 610 - y_coor, fill="black", width=1)  # Heading

def create_possible_route_line(angle_in):
    angle = -(angle_in) + 61.5+28.5
    x_coor = (cos(angle * pi / 180) * 550)
    y_coor = (sin(angle * pi / 180) * 550)
    w.create_line(310, 610, 310 - x_coor, 610 - y_coor, fill="yellow", width=1, arrow=tk.LAST)  # Heading


def find_best_route(ob_points):
    clear_path_points = []

    for ob_point in ob_points:
        if ob_point[3] > 590:
            clear_path_points.append(ob_point)

    count = len(clear_path_points)

    start_index = 0

    for x in range(count):
        if x + 1 != count:
            if clear_path_points[x][4] + 1 != clear_path_points[x+1][4]:
                #print("First_angle: ", clear_path_points[start_index][2], " Second Angle: ", clear_path_points[x][2])
                create_angle_line(clear_path_points[start_index][2])
                create_angle_line(clear_path_points[x][2])
                possible_angle = (clear_path_points[start_index][2] + clear_path_points[x][2]) / 2
                create_possible_route_line(possible_angle)
                start_index = x + 1
        else:
            #print("First_angle: ", clear_path_points[start_index][2], " Second Angle: ", clear_path_points[x][2])
            create_angle_line(clear_path_points[start_index][2])
            create_angle_line(clear_path_points[x][2])
            possible_angle = (clear_path_points[start_index][2] + clear_path_points[x][2]) / 2
            create_possible_route_line(possible_angle)
            start_index = x + 1

    if count == 0:
        print("No free routes - Start search algorithm")

