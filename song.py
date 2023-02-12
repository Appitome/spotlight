import followspot as fs
import display as dp
import configparser
import time
import glob

#Get the current display settings from the ini file
config = configparser.ConfigParser()
def collect_settings(initial = False):
    global grid_x
    global grid_y
    global config_path
    
    if initial:
        ini_files = glob.glob('*.ini')
        config_path = ini_files[0]

    config.read(config_path)

    if initial:
        grid_x = int(config['DISPLAY']['display_height'])
        grid_y = int(config['DISPLAY']['display_width'])

    return config['USERS']['current_user']

collect_settings(initial = True)

while True:
  
  #Get the current user to pull song data for
  current_user = collect_settings()
  
  #Check if access token is expired - auto refresh if expired
  fs.access_expired(current_user, auto_refresh = True)
  
  #Collect current user song info
  data = fs.refresh_current_data(current_user)
  
  #Check if the user is currently playing on account
  if data and fs.is_playing(data):

    #Check what type of audio is currently playing
    play_type = fs.play_type(data)
    
    #If a song (track) is playing
    if play_type == 'track':
      if fs.new_song(data):
        print("")
        #Check if the song has changed from last
        print(fs.song_name(data))
        #Download the new ablum cover
        fs.download_ablum_cover(data, "CurrentlyPlaying.jpg")
        #Modify the downloaded cover to fit display specs
        dp.gridify(grid_x,grid_y,"CurrentlyPlaying.jpg",scramble=True)
      
    #If a podcast (episode) is playing
    elif play_type == 'episode':
      print('episode')
      time.sleep(10)
    
    #If an ad is playing
    elif play_type == 'ad':
      print('ad')
      time.sleep(10)
  
  #If user is not currently playing on account
  else:
    #print("Extended Sleep")
    if dp.display_timeout(30,180):
      fs.new_song(reset = True)
      print('')
      print("timeout elapsed")
      dp.gridify(grid_x,grid_y,"timeout.jpg",scramble=True)
    
    print("|", end="",flush=True)
    time.sleep(10)
    
  time.sleep(0.5)