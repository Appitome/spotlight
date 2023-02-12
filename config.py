import configparser
import os
import time
import followspot as fs


file_path = "config.ini"

config = configparser.ConfigParser()

def config_display(display_type = None, display_height = None, display_width = None, displey_brightness = None, animate_time = None):
    
    if display_type == None:
        while True:
            display_type = input("Enter the display type (Address/Matrix): ")
            if display_type == "address" or display_type == "Address":
                display_type = "address"
                break
            elif display_type == "matrix" or display_type == "Matrix":
                display_type = "matrix"
                break
    
    if display_height == None:
        display_height = input("Enter the display height: ")
        print("Height set to:", display_height)
    
    if display_width == None:
        display_width = input("Enter the display width: ")
        print("Width set to:", display_width)
    
    if displey_brightness == None:
        while True:
            displey_brightness = input("Enter the display brightness: ")
            if int(displey_brightness) <= 100:
                break
    
    if animate_time == None:
        animate_time = input("Enter the transition animation time: ")


    display['display_type'] = display_type
    display['display_height'] = str(display_height)
    display['display_width'] = str(display_width)
    display['displey_brightness'] = str(displey_brightness)
    display['animate_time'] = str(animate_time)

def initilize():
    print("Time To Set Up Your New Display!")
    time.sleep(0.5)
    print("First, Lets Set Up Your Spotify Account")
    time.sleep(0.5)
    username = input("Please Enter Your Username: ")
    users['owner'] = username
    users['Current_user'] = username
    users['users'] = username
    
    fs.initialize_token(username = username)
    
    print("Great! Your Account Is Now Set Up!")
    time.sleep(0.5)
    print("Next Let's Set Up The Display")
    config_display(displey_brightness = 100, animate_time = 0.3)
    time.sleep(0.5)
    print("You're All Set!")
    time.sleep(0.5)
    print("Run 'main.py' And Start Playing A Song To Test Out Your New Display")
    time.sleep(0.5)
    print("Once Youre Happy With Your Display Settings Follow The Instructions To Have The Display Run On Startup")
    time.sleep(0.5)
    print("Remember, Run 'config.py' To Change Any Settings Or Add New Users")

def add_users():
    users = fs.get_users()
    print("Current Users:", users)

    username = input("Please Enter New Username: ")
    
    if username in users:
        print("username already exists")
    else:
        
        fs.initialize_token(username = username)
        
        config['USERS']['users'] = str(fs.get_users())

        with open(file_path, 'w') as configfile:
            config.write(configfile)

        print(f"User {username} has been added")

def remove_users(): 

    #Get owner info
    owner = config['USERS']['owner']

    users = fs.get_users()
    print("Current Users:", users)

    username = input("Type the user ID to remove: ")
    remove_cache = username + ".cache"
    
    #If username is found
    if os.path.exists(remove_cache):

        #Ensure owner will not be deleted
        if owner == username:
            #Cannot delete owner
            print(f"{username} is this device's owner. The owner cannot be removed")
            exit()

        #Delete Conformation
        if 'DELETE' == input(f"Type 'DELETE' to remove user {username}: "):
            #Make owner the current user
            config['USERS']['current_user'] = owner
            #Delete .cache file
            os.remove(remove_cache)
            #Update users
            config['USERS']['users'] = str(fs.get_users())
            #Save changes to .ini file
            with open(file_path, 'w') as configfile:
                config.write(configfile)
            
            print(f"User {username} has been removed")

def reset_settings():
    print("WARNING: Reset will remove all users and settings")
    #Reset Conformation
    if 'RESET' == input(f"Type 'RESET' to restore device to default: "):

        users = fs.get_users()
        for username in users:
            remove_cache = username + ".cache"
            os.remove(remove_cache)

        print("Device reset. Reboot to continue")

        while True:
            try:
                os.remove(file_path)
            except:
                exit()

        

def settings():

    print("Settings:")
    print("1: Add Users")
    print("2: Remove Users")
    print("3: Edit Display")
    print("4: RESET")
    print("5: Exit")

    response = int(input("(1-5): "))

    if response == 1: #Add Users
        print("You entered 1.")
        add_users()
    elif response == 2: #Remove Users
        print("You entered 2.")
        remove_users()
    elif response == 3: #Edit Display
        print("You entered 3.")
        config_display()
    elif response == 4: #Reset config
        print("You entered 4.")
        reset_settings()
    else:
        #the response is not in the list
        exit()

if os.path.exists(file_path):
    print(file_path, "Exists")
    
    config.read(file_path)

    display = config['DISPLAY']
    users = config['USERS']
    
    print(display['display_type'])
    settings()
else:
    config['DISPLAY'] = {}
    config['USERS'] = {}
    display = config['DISPLAY']
    users = config['USERS']
    initilize()

with open(file_path, 'w') as configfile:
  config.write(configfile)