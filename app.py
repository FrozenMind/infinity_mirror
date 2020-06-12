from time import sleep
from neopixel import *
import argparse
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from flask import Flask, request, render_template

# LED strip configuration:
LED_COUNT      = 91      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
MODE_BUTTON_PIN = 16

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(MODE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set 

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

break_mode = False

def break_running_mode():
    global break_mode
    break_mode = True
    sleep(0.2)
    break_mode = False

def set_color(color):
    break_running_mode()
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def start_wipe(color):
    break_running_mode()
    for i in range(strip.numPixels()):
        if break_mode == True:
            return
        strip.setPixelColor(i, color)
        strip.show()
        sleep(0.05)

# start webserver

app = Flask(__name__, template_folder='client', static_folder='client')

@app.route('/color', methods=['PUT'])
def color():
    green = int(request.form['green'])
    red = int(request.form['red'])
    blue = int(request.form['blue'])
    color = Color(green, red, blue)
    print('set color', color)
    set_color(color)
    return 'OK'

@app.route('/wipe', methods=['PUT'])
def wipe():
    green = int(request.form['green'])
    red = int(request.form['red'])
    blue = int(request.form['blue'])
    color = Color(green, red, blue)
    print('wipe to color', color)
    start_wipe(color)
    return 'OK'
