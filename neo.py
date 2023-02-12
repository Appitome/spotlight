import time
import board
import neopixel
import pickle

################
#NEOPIXLES
NEO_PIXEL_COUNT = 64
NEO_PIXEL_PIN = board.D18

#Define image transition speed
ANIMATE_TIME = 0.5
################

#Initialize the neopixels
neopixels = neopixel.NeoPixel(NEO_PIXEL_PIN, NEO_PIXEL_COUNT, brightness = 100, auto_write=True)

#Testing fill
#neopixels.fill((255,255,255))
#neopixels.brightness = 0.75

def display():
    # Open the pickle file
    with open("CurrentOutput.pickle", "rb") as f:
        data = pickle.load(f)

    for position in data:
        p = position[0]
        neopixels[p] = position[1]
        
        time.sleep(ANIMATE_TIME/len(data))