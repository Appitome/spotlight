import os
import time
import pickle
import configparser
from rgbmatrix import RGBMatrix, RGBMatrixOptions

#File to monitor
file_path = 'CurrentOutput.pickle'

config = configparser.ConfigParser()
def collect_settings():
    global grid_x
    global grid_y
    global displey_brightness
    global animate_time
    
    for file in os.listdir():
        if file.endswith(".ini"):
            config_path = os.path.abspath(file)

    config.read(config_path)

    grid_x = int(config['DISPLAY']['display_height'])
    grid_y = int(config['DISPLAY']['display_width'])
    displey_brightness = int(config['DISPLAY']['displey_brightness'])
    animate_time = float(config['DISPLAY']['animate_time'])

def set_matrix():
    global matrix

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = grid_x
    options.cols = grid_y
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'
    options.brightness = displey_brightness
    #options.gpio_slowdown = 0
    options.pwm_lsb_nanoseconds = 100
    options.scan_mode = 1

    #Define the matrix
    matrix = RGBMatrix(options = options)

def monitor(file_path):
    global i_time
    #Check the modification time of the file
    c_time = os.path.getmtime(file_path)

    #If the file has been modified since the last check
    if c_time > i_time:
        print('The file has been updated')
        display()
        # Update the initial time
        i_time = c_time

def display():
    # Open the pickle file
    with open(file_path, "rb") as f:
        while True:
            try:
                data = pickle.load(f)
                break
            except:
                time.sleep(0)

    for position in data:
        #print(position[0])
        r,g,b = position[1]
        x,y = position[2]
        matrix.SetPixel(x, y, r, g, b)
        
        time.sleep(animate_time/len(data))

#wait for data file to exist
while os.path.exists(file_path) is not True:
    print("i_time file does not exist yet")
    time.sleep(3)

#Get the initial modification time of file
i_time = os.path.getmtime(file_path)

#Get Matrix Settings
collect_settings()

#Define Matrix
set_matrix()

while True:
    monitor(file_path)
    time.sleep(0)


