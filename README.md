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

# Spotlight

## Spotify Developer account
To use the display, a spotify developer account must be set up to collect information

This account can be created with a prexisting spotify streaming account

Log into the developer dashboard
```
https://developer.spotify.com/dashboard/login
```
Create a new 'app' to generate user creditials

After the 'app' is created, the overview page is accessable. Both the Client ID and Client Secret can be found on this page. They will be needed when configuring the display.

![Overview](https://user-images.githubusercontent.com/17167742/218382264-190fc29e-2a77-4e25-8387-cca5bc393f51.png)

### Edit Settings

In the 'Edit Settings' tab, add a localhost address. Most four digit numbers will work. For this example:
```
http://localhost:8080/callback/
```
![Localhost](https://user-images.githubusercontent.com/17167742/218383460-f018329e-b116-44f9-8eff-b96dce00ef5b.png)

### Users And Access 

To connect to Spotify accounts in developer mode, they must be specified in the 'Users And Access' tab. Select 'Add New User' and ender the email that is connected to the Spotify account you wish to connect. The specified accounts can be authenticated with the 'app'

After setting up the developer app, the following items will be needed during the display configuration to link Spotify accounts:
1. Client ID
2. Client Secret
3. Localhost Address

## Raspberry Pi Imager
Download use the raspberry pi imager from the official raspberry pi website:
``` 
https://www.raspberrypi.com/software/ 
```

Once downloaded, insert the micro sd card and open the imager

![Pi_Imager](https://user-images.githubusercontent.com/17167742/218379092-2583721e-726c-4e05-af0f-ef718cad930f.png)

### Select an operating system
Select the recomended destop version for the raspberry pi

### Choose storage device
Select the micro sd card from the menu - **The selected storage device will be reformatted**

### Advanced settings
Select the gear in the lower righthand corner to access the advanced settings

![Advanced_Settings](https://user-images.githubusercontent.com/17167742/218379529-c274369a-9308-41f8-9a5e-ed251b5ba2fe.png)

* Set the hostname - *raspberrypi* (for example)
* Enable SSH communication
* Set raspberry pi username - *pi* (for example)
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
python installer.py
```
 - During the setup process some questions will be asked
   - ***y*** continue, ***y*** continue, ***1*** RGB Matrix Bonnet, ***1*** Quality, ***y*** continue
 - If asked to reboot, select the '***no***' option. The program will manually reboot once finished.

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
The first time the config program is run it will automatically walk through the setup process. The owner's account should always be set up first:
1. Enter username
2. Enter the Cliet Id from the Spotify Developer Account Overview
3. Enter the Cliet Secret from the Spotify Developer Account Owerview (Click 'Show Client Secret' if not visable)
4. Enter the Localhost (Redirect) Address specified in the Spotify Developer Settings

Once all of the correct credentials have been entered, the terminal will generate a URL. Copy this URL into an incognito web browser. You will then be prompted to log into your spotify account. If successful, the browser will generate a http localhost link in the search bar. Copy this link and paste it back into the terminal.
   - Incognito mode is used to prevent the browser from automatically logging into a previously known account
   - Right click to paste into terminal

Next, the program will ask questions to correctly initialize the display
1. Enter display pixel type - This will be either 'matrix' for a matrix display or 'address' for addressable LEDs
2. Enter display height (pixels)
3. Enter display width (pixels)

If everything is correctly configured, the program will adjust the settings and prompt the next steps.


