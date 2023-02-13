import os
import sys
import shutil
import requests
import subprocess


def suto(package):
     print("")
     print("SUDO: " + package)
     subprocess.check_call(["sudo", "apt-get", package])

# suto("update")
# suto("upgrade")

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

#Install matrix files
response = requests.get("https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh")
with open("rgb-matrix.sh", "w") as file:
    file.write(response.text)
subprocess.run(["sudo", "bash", "rgb-matrix.sh"])

#Extract rgbmatrix file
if os.path.exists('rgbmatrix') == False:

    src_path = 'rpi-rgb-led-matrix/bindings/python/rgbmatrix'
    dst_path = os.path.join(os.getcwd(), os.path.basename(src_path))

    shutil.copytree(src_path, dst_path)

#Remove extra matrix files
if os.path.exists('rgb-matrix.sh'):
    os.remove('rgb-matrix.sh')
if os.path.exists('rpi-rgb-led-matrix'):
    shutil.rmtree('rpi-rgb-led-matrix')


#Reboot once all modules are installed
print('Rebooting System')
print('Please wait a few minutes before trying to connect to device')
os.system("sudo reboot") 
