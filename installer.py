import sys
import subprocess
import os


def suto(package):
    print("")
    print("SUDO: " + package)
    subprocess.check_call(["sudo", "apt-get", package])

suto("update")
suto("upgrade")

def sutoinst(package):
    print("")
    print("SUDO INSTALL: " + package)
    subprocess.check_call(["sudo", "apt-get", "install", package])

sutoinst("python3-pip")

print("")
print("INSTALLLING: neopixel")
os.system('sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel')
os.system('sudo python3 -m pip install --force-reinstall adafruit-blinka')

def install(package):
    print("")
    print("INSTALLLING: " + package)

    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
 
install("Pillow")
#install("rpi_ws281x")
#install("neopixel")

#Reboot once all modules are installed
print('Rebooting System')
os.system("sudo reboot")