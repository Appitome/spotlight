# spotlight

# The largest heading
## The second largest heading
###### The smallest heading

**This is bold text**

*This text is italicized*

**This text is _extremely_ important**

***All this text is important***

<sub>This is a subscript text</sub>

<sup>This is a superscript text</sup>

> Text that is a quote

```this is a code snippit```

```
this is a code line
```

* bullet point
1. list item
   - First nested list item
     - Second nested list item
     
<!-- This content will not appear in the rendered Markdown -->

![timeout](https://user-images.githubusercontent.com/17167742/218343569-84170373-cc79-4d65-9a79-e10e276c8415.jpg)



## Raspberry Pi Imager
Download use the raspberry pi imager from the official raspberry pi website:
``` https://www.raspberrypi.com/software/ ```

Once downloaded, insert the micro sd card and open the imager

### Choose an operating system
Select the recomended destop version for the raspberry pi

### Choose storage device
Select the micro sd card from the menu

**The selected storage device will be reformatted**

### Advanced settings
Select the gear in the lower righthand corner to access the advanced settings
* Set the hostname - *raspberrypi* for example
* Enable SSH communication
* Set raspberry pi username - *pi* for example
* Set raspberry pi password
* Enter wifi username and password
   - The pi zero w only works with 2.4ghz networks. Not compatible with 5ghz

After veryfying the above configurations write to the sd card. - this process may take some time to complete

Once completed, insert the newly flashed sd card into the pi and power on - the pi will need some time to boot

## Connecting to the Raspberry Pi
Communication to the raspberry pi can be performed through a SSH connection

SSH can be performed from the terminal of a computer that is connected to the same network as the pi

 - Command prompt (Windows)
 - Terminal (Mac)

First check if the raspberry pi can be found on the network

In the terminal:
```
ping raspberrypi.local
```
If connected, the ping will return an address. Sometimes the Pi might take longer to boot so if no responce is initally found wait a couple minutes and try again.

If the ping continously fails to connect, first make sure the pi has a sufficient power source. Additionally, double check the Imager settings, ensuring that the Wifi SSID and hostname is correct.

Once a ping communication has successfully completed, confirming the Pi is online, the SSH communication can be established.

In the terminal:
```
SSH pi@raspberrypi.local
```
Select "yes" and enter the previously set password for the device.

If a known host safty error occurs follow the terminal instructions to clear the ```known_hosts``` file on the computer being used

## Cloning the Git Repository

Clone the spotlight repository using the following command:
```
git clone https://github.com/Appitome/spotlight.git
```
Once cloned we can access the spotlight folder:
```
cd /home/pi/spotlight
```
Inside this folder, all files can be viewed using the command:
```
ls
```
A couple of modules are required to be installed before the main program can be run. Enter the following command:
```
python setup.py
```
 - During the setup process some questions may be asked. If asked to reboot, select the 'no' option. The program will manually reboot once finished.
Once the terminal prompts that the Pi is rebooting, allow a couple minutes for the device to boot.

To check that the Pi has successfullly rebooted, ping to confirm, reconnect using SSH, and reaccess the working directory
```
ping raspberrypi.local
```
```
SSH pi@raspberrypi.local
```
```
cd /home/pi/spotlight
```
## Configure Display Settings
To setup the display run the configuration program:
```
python config.py
```
