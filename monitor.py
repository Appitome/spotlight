import RPi.GPIO as GPIO
import os
import ast
import time
import configparser
import display as dp
import followspot as fs

config = configparser.ConfigParser()

#Set the GPIO mode
GPIO.setmode(GPIO.BCM)

#Define the GPIO pin input
GPIO_SW = 25

#Set the GPIO pin as an input
GPIO.setup(GPIO_SW, GPIO.IN)

#Callback function
def switch_user(channel):
    
    for file in os.listdir():
        if file.endswith(".ini"):
            config_path = os.path.abspath(file)
    config.read(config_path)

    current_user = config['USERS']['current_user']
    users = config['USERS']['users']
    grid_x = int(config['DISPLAY']['display_height'])
    grid_y = int(config['DISPLAY']['display_width'])

    #Convert users data back to list
    users = ast.literal_eval(users)

    print("Current user:", current_user)
    print("Users:", users)

    #Find current user in users list
    index = users.index(current_user)
    
    #Move to next user
    index += 1
    #If we've reached end of list, reset the index to 0
    if index >= len(users):
        index = 0

    #Set new current user
    print("New current user:", users[index])
    config['USERS']['current_user'] = users[index]

    #Save changes to .ini file
    with open(config_path, 'w') as configfile:
        config.write(configfile)

    print("")

    fs.download_profile_picture(users[index], "CurrentUser.jpg", request_timeout = 60)
    dp.crop_gridify("CurrentUser.jpg", grid_x, grid_y, scramble = True)

# Add the event detection for a falling edge on the GPIO_CLK pin
GPIO.add_event_detect(GPIO_SW, GPIO.RISING, callback=switch_user, bouncetime=500)
    #GPIO.FALLING
    #GPIO.RISING
    #GPIO.BOTH

# Continuously monitor for events
while True:
    time.sleep(1)