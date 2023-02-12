from PIL import Image
import pickle
import random
import time

def gridify(grid_x,grid_y,file_location,scramble=False): #Resizes image and converts it to RGB format
  
  #Try to open the image and resize it to pixels
  try:
    im = Image.open(file_location)
    im = im.resize((grid_x, grid_y))
  except:
    print("file not found:", file_location)
    return(False)
  
  # Save the image as a JPEG file
  im.save('CurrentOutput.jpg', 'JPEG')

  # Create a list of pixels in the image  
  pixels = list(im.getdata())

  # Simplify the pixels to a color grid
  grid = [pixels[i*grid_x : i*grid_x + grid_x] for i in range(grid_y)]

  # Flatten the grid into a single list of colors
  #flattened = [color for row in grid for color in row]

  # Flatten the grid into a single list of colors with position and coordinates
  flattened = [((x+(y*grid_y)), color, (x, y)) for y, row in enumerate(grid) for x, color in enumerate(row)]
  #print(flattened)

  if scramble == True:
    random.shuffle(flattened)

  # serialize the data
  with open("CurrentOutput.pickle", "wb") as f:
    pickle.dump(flattened, f)

def crop_gridify(file_location, grid_x,grid_y, scramble=False): #Crops image to center and converts to RGB format
  
  #Try to open the image and resize it to pixels
  try:
    im = Image.open(file_location)
  except:
    print("file not found:", file_location)
    return(False)

  width, height = im.size
  min_dim = min(width, height)

  # Crop the image to a 100x100 square centered in the middle of the image
  left = (width - min_dim) / 2
  top = (height - min_dim) / 2
  right = (width + min_dim) / 2
  bottom = (height + min_dim) / 2
  im = im.crop((left, top, right, bottom))

  im = im.resize((grid_x, grid_y))

  # Save the image as a JPEG file
  im.save('CurrentOutput.jpg', 'JPEG')

  # Create a list of pixels in the image  
  pixels = list(im.getdata())

  # Simplify the pixels to a color grid
  grid = [pixels[i*grid_x : i*grid_x + grid_x] for i in range(grid_y)]

  # Flatten the grid into a single list of colors
  #flattened = [color for row in grid for color in row]

  # Flatten the grid into a single list of colors with position and coordinates
  flattened = [((x+(y*grid_y)), color, (x, y)) for y, row in enumerate(grid) for x, color in enumerate(row)]
  #print(flattened)

  if scramble == True:
    random.shuffle(flattened)

  # serialize the data
  with open("CurrentOutput.pickle", "wb") as f:
    pickle.dump(flattened, f)

start_time = time.time()
last_time = start_time
timeout_bool = True
def display_timeout(cycle_time, timeout_time): #Timeout program that turns the display off after an allotted amount of time has elapsed
  #cycle_time is the maximum time allowed between cycles before the counter assumes a song has been playing and resets
  #timeout_time is the durration of the timout that must elapse before the display is turned off
  
  global start_time
  global last_time
  global timeout_bool

  current_time = time.time()
  
  #Check the time between cycle
  cycle_difference = current_time - last_time
  #If there has been an extended time period between timeout readings
  if cycle_difference >= cycle_time: #Difference cannot be larger then cycle delay
    #Reset the start time
    start_time = current_time
    timeout_bool = True
    print("")
    print("start time reset")

  #Check the current timer length from start
  time_difference = current_time - start_time
  if timeout_bool and time_difference >= timeout_time:
    #If the timeout has elapsed

    #TIMEOUT ACTIONS HERE

    timeout_bool = False
    return True

  #Set last_time equal to the current time for the next cycle
  last_time = current_time
