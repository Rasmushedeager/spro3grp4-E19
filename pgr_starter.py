import board
import digitalio
import os
import subprocess
import time
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
prev_value = True
print("inital button value:", button.value)
while 1:
    button = digitalio.DigitalInOut(board.D4)
    button.direction = digitalio.Direction.INPUT
    x = button.value
    if x and prev_value != x:
        #subprocess.Popen("sudo python3 /home/tobiasravn/Desktop/code_pc/main.py 1", shell=True)
        #subprocess.call(['xterm', '-e', 'python bb.py'], cwd='/home/tobiasravn/Desktop/code/', shell =True)
        subprocess.call(["gnome-terminal", "-e", "sudo python3 /home/tobiasravn/Desktop/code_pc/main.py"])
        while button.value:
            pass
        print("Whaiting to clean up the program...")
        time.sleep(3)
        
    prev_value = x

       


