import os
import json
import requests
from PIL import Image
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

#https://developer.spotify.com/documentation/web-api/reference/#/operations/get-the-users-currently-playing-track

def initialize_token(client_id = None, client_secret = None, redirect_uri = None, username= None):  #Setup for first time use - Authorizes user and generates refresh token
  
  if username == None:
    username = input("Enter new username: ")
  if client_id == None:
    client_id = input("Enter Client Id: ")
  if client_secret == None:
    client_secret = input("Enter Client Secret: ")
  if redirect_uri == None:
    redirect_uri = input("Enter Redirect URI: ")

  scope = "user-read-currently-playing" # scope of the access needed
  auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
  
  print("Paste the following URL into your browser: ")
  print(auth_url)

  url = input("Please paste the generated authorization URL from browser: ")
  
  try:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    auth_code = query_params['code'][0]
  except:
    print("")
    print("Authorization Code FAILED... Please Try Again")
    print("")
    quit()

  print("Authorization code: ", auth_code)

  #request an access token and a refresh token
  payload = {
      "grant_type": "authorization_code",
      "code": auth_code,
      "redirect_uri": redirect_uri,
      "client_id": client_id,
      "client_secret": client_secret
  }

  response = requests.post("https://accounts.spotify.com/api/token", data=payload)

  if response.status_code == 200:
    data = response.json()
    print(data)
    access_token = data["access_token"]
    expires_in = data["expires_in"]
    refresh_token = data["refresh_token"]
    print("Access token: ", access_token)
    print("Refresh token: ", refresh_token)
  else:
    print("Error: ", response.status_code)
    print(response.text)
    exit()

  # Get the current system time
  now = datetime.now()
  # Calculate the expiration time of the access token
  expiration_time = now + timedelta(seconds=expires_in)
  # Print the expiration time of the access token
  print("Access token expires at: ", expiration_time)
  expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M")
  print(expiration_time_str)

  # Create a dictionary containing the user's information
  user_info = {
    "username": username,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret,
    "refresh_token": refresh_token,
    "access_token" : access_token,
    "expiration_time" : expiration_time_str
  }

  # Create a file name using the username and the .cache extension
  file_name = username + ".cache"
  
  # Write the JSON object to a file
  with open(file_name, "w") as f:
      f.write(json.dumps(user_info))
  
  
  return(refresh_token, access_token)

def get_users():   #Returns a list of all the current user cache files
  path = os.getcwd()
  cache_files = [f.replace('.cache','') for f in os.listdir(path) if f.endswith('.cache')]
  #print(cache_files)
  return cache_files

def collect_current_user(username):   #Collects user cache data to be accessed
  file_name = username + ".cache"

  if not os.path.isfile(file_name):
    print(f"{file_name} does not exists.")
    return(False)

  #Load user_info from the file
  with open(file_name, "r") as f:
    user_info_json = f.read()
    user_info = json.loads(user_info_json)
    return user_info

def access_expired(username, auto_refresh = False):   #Check the acces code expiration_time stored in the user cache. Option to auto refresh 
    
  user_info = collect_current_user(username)

  if user_info is False:
    exit()

  expiration_time_str = user_info["expiration_time"]
  
  #Convert expiration_time_str to a datetime object
  expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M")

  #Get the current system time
  now = datetime.now()

  # Compare the current system time with the expiration time
  if now >= expiration_time and auto_refresh:
    print(f"Auto refreshing access token")
    refresh_access_token(username)
  elif now >= expiration_time and not auto_refresh:
    print(f"Access token has expired")
    return(True)
  else:
    #print("Access token is still valid")
    return(False)

def refresh_access_token(username, request_timeout = 60):   #Generate a new access token using the refresh token
  
  file_name = username + ".cache"

  user_info = collect_current_user(username)

  if user_info is False:
    exit()
  
  #set up the request payload
  payload = {
    "grant_type": "refresh_token",
    "refresh_token": user_info['refresh_token'],
    "client_id": user_info['client_id'],
    "client_secret": user_info['client_secret']
  }

  try:
    #make request to the Spotify authorization server
    response = requests.post("https://accounts.spotify.com/api/token", data=payload, timeout=request_timeout)
  except requests.exceptions.Timeout as e:
    print ("Timeout Error:", e)
    return(False)
  
  #if the request is successful return the new access token
  if response.status_code == 200:
    #parse the response as JSON
    data = response.json()
    access_token = data["access_token"]
    expires_in = data["expires_in"]

    # Get the current system time
    now = datetime.now()
    # Calculate the expiration time of the access token
    expiration_time = now + timedelta(seconds=expires_in)
    # Print the expiration time of the access token
    expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M")
    
    with open(file_name, "w") as f:
      user_info["access_token"] = access_token
      user_info["expiration_time"] = expiration_time_str
      f.write(json.dumps(user_info))
    
    #print the access token
    print("")
    print(f"Access Token Expires In {expires_in/60} Minutes")
    #return the access token
    return(access_token)
  else:
    # The request was unsuccessful, print the status code and error message
    print("Error: " + str(response.status_code))
    print(response.text)
    return(False)

def refresh_current_data(username, request_timeout = 60):  #Retrieve the latest Spotify currently playing information
  
  user_info = collect_current_user(username)

  if user_info is False:
    exit()

  access_token = user_info["access_token"]
  
  if access_token:
    #set up the request headers with access token
    headers = {
      "Authorization": "Bearer " + access_token
    }
    #print("headers: ", headers)

    try:
      #make a request to the Spotify Web API
      response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers, timeout=request_timeout)
    except requests.exceptions.Timeout as e:
      print(f"Timeout Error:", e)
    except:
      print(f"Request Error")

    if (response.status_code == 200):
      #print the response
      #print(response.json())
      #return the response
      return response.json()
    elif(response.status_code == 204):
      #Code 204 means account is not currently playing: returns False
      #print(response.status_code)
      #print("Playback not available or active")
      return False
    else:
      #print the response status code
      print(f"Response status code error:",response.status_code)
      
      #204: Playback not available or active
      #401: Bad or expired token. This can happen if the user revoked a token or the access token has expired. You should re-authenticate the user.
      #403: Bad OAuth request (wrong consumer key, bad nonce, expired timestamp...). Unfortunately, re-authenticating the user won't help here.
      #429: The program has exceeded its rate limits.

  else:
    print(f"Error refreshing access token")

def is_playing(currently_playing):  #Get current play status
  
  try:
    return(currently_playing["is_playing"])
  except:
    print("Unable to read data (Bad data)")
    return(False)

def play_type(currently_playing):   #Check what type of audio is currently playing
  #Can be one of: track, episode, ad or unknown
  cp = currently_playing["currently_playing_type"]
  #return the song type
  return(cp)

def song_name(currently_playing):  #Get the name of the audio that is currently playing
    if currently_playing["currently_playing_type"] == "track":
        song_title = currently_playing["item"]["name"]
        #return the song title
        #print(song_title)
        return song_title    
    else:
        print("Current Play Type Is Not 'track'")
        return False

currentsong = False
def new_song(currently_playing = None, reset = False):  #Checks if the current song is the same as last song checked 
  global currentsong 

  if reset:
    currentsong = False
    return

  if currentsong != song_name(currently_playing):
    currentsong = song_name(currently_playing)
    return(True)
  else:
    return(False)

def download_ablum_cover(currently_playing, file_location):  #Downloads the curently playing album cover to specified location
  
  try:
    # Get the album cover image URL
    album_cover_url = currently_playing["item"]["album"]["images"][0]["url"]
    # 0 = 640x640
    # 1 = 300x300
    # 2 = 64x64

    # Download the album cover image
    album_cover_image = Image.open(requests.get(album_cover_url, stream=True).raw)

    # Save the album cover image to a file
    album_cover_image.save(file_location)

  except:
    print("No Ablum Cover Available")
    return(False)

def download_profile_picture(username, file_location, request_timeout = 60):  #Creates a seperate API call to collect user profile picture
  
  access_expired(username, auto_refresh = True)
  
  user_info = collect_current_user(username)

  access_token = user_info["access_token"]
  
  if access_token:
    #Set request headers with access token
    headers = {
      "Authorization": "Bearer " + access_token
    }

    try:
      #Make a request to the Spotify Web API
      response = requests.get("https://api.spotify.com/v1/me", headers=headers, timeout=request_timeout)
    except requests.exceptions.Timeout as e:
      print(f"Timeout Error:", e)
    except:
      print(f"Request Error")

    data = json.loads(response.text)
    #Parse the JSON data from the response
    data = json.loads(response.text)
    #Get the user's profile image
    profile_url = data["images"][0]["url"]

    #Download the profile image
    profile_image = Image.open(requests.get(profile_url, stream=True).raw)

    #Save the album cover image to a file
    profile_image.save(file_location)

def play_progress(currently_playing):   #Get the current play percentage of the current track
  progress = currently_playing["progress_ms"]
  duration = currently_playing["item"]["duration_ms"] 
  percentage = (progress / duration) * 100
  print(round(percentage, 1),"%")
  return(percentage)    

