import followspot as fs
import display as dp
import time

current_user = "ROB"

#fs.initialize_token(client_id = '0f0d52e0e2c24a988dcbcc55a9d249ab', client_secret = 'c1c98444cdea4ea2a38675f58f1d1a10', redirect_uri = 'http://localhost:8888/callback/', username= 'r')

#generate new access token
#access_token = fs.refresh_access_token(current_user)
#print("Access Token:", access_token)

fs.access_expired(current_user, auto_refresh = True)

fs.get_users()

#request currently playing data from servers
data = fs.refresh_current_data(current_user)
#print(data)

print("Is Playing:", fs.is_playing(data))

while True:
  
  fs.access_expired(current_user, auto_refresh = True)
  
  data = fs.refresh_current_data(current_user)
  
  if fs.is_playing(data):

    play_type = fs.play_type(data)
    
    if play_type == 'track':
      if fs.new_song(data):
        print("")
        print(fs.song_name(data))
        fs.download_ablum_cover(data, "CurrentlyPlaying.jpg")
        dp.gridify(64,64,"CurrentlyPlaying.jpg",scramble=True)
      
      #fs.play_progress(data)

    elif play_type == 'episode':
      print('episode')
      time.sleep(10)
    
    elif play_type == 'ad':
      print('ad')
      time.sleep(10)

  else:
    print("Extended Sleep")
    time.sleep(10)
    
  time.sleep(0.5)


#see what type of audio is playing (ie. "track")
play_type = fs.play_type(data)
print("We are currently listening to", play_type)

#get song name if available
song = fs.song_name(data)
if song is not False:
  print(song)
else:
  print("Song is not currently playing")

if song == "track":

  fs.download_ablum_cover(data, "CurrentlyPlaying.jpg")

  fs.gridify(32,32,"CurrentlyPlaying.jpg")