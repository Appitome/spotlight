import os
import time
import subprocess
import configparser
import urllib.request
import multiprocessing

#Change working directory to folder
os.chdir('/home/pi/spotlight/')

def connected(): #Check if connected to the internet
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

#Clear terminal
os.system('cls||clear')
print("connecting...",end="")
#Wait for connection
while not connected():
    print(".",end="")
    time.sleep(2)
print("")    
time.sleep(0.5)

#Define function that will be run in a separate subprocess
def subprocess_0():
    while True:
        subprocess.run(["python", "song.py"])

def subprocess_1(): #Set the display program to run
    while True:    
        config = configparser.ConfigParser()

        for file in os.listdir():
            if file.endswith(".ini"):
                config_path = os.path.abspath(file)
        
        config.read(config_path)

        display_type = config['DISPLAY']['display_type']

        if display_type == 'matrix':
            subprocess.run(["sudo", "python", "matrix.py"])
        elif display_type == 'address':
            subprocess.run(["sudo", "python", "neo.py"])
        else:
            print("Headless Mode")

def subprocess_2(): #Program to monitor external events
    while True:
        subprocess.run(["python", "monitor.py"])
        
 
# Create Process objects
p0 = multiprocessing.Process(target=subprocess_0)
p1 = multiprocessing.Process(target=subprocess_1)
p2 = multiprocessing.Process(target=subprocess_2)

# Start the subprocesses
p0.start()
p1.start()
p2.start()