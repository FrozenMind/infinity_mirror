from time import sleep
from neopixel import *
import argparse
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from flask import Flask, request, render_template
import random
import math

# LED strip configuration:
LED_COUNT = 91      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
MODE_BUTTON_PIN = 16

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
# Set pin 10 to be an input pin and set
GPIO.setup(MODE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                          LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

break_mode = False


def break_running_mode():
    global break_mode
    break_mode = True
    sleep(0.2)
    break_mode = False


def set_pixel(i,  green, red, blue):
    strip.setPixelColor(i, Color(green, red, blue))


def set_all(green, red, blue):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(green, red, blue))
    strip.show()


# start webserver
app = Flask(__name__, template_folder='client', static_folder='client')


# functions that control the led strip
@app.route('/color', methods=['PUT'])
def color():
    green = int(request.form['green'])
    red = int(request.form['red'])
    blue = int(request.form['blue'])
    print('set color', color)
    break_running_mode()
    set_all(green, red, blue)

    return 'OK'


@app.route('/wipe', methods=['PUT'])
def wipe():
    green = int(request.form['green'])
    red = int(request.form['red'])
    blue = int(request.form['blue'])
    print('wipe to color', color)
    break_running_mode()
    for i in range(strip.numPixels()):
        if break_mode == True:
            return
        strip.setPixelColor(i, Color(green, red, blue))
        strip.show()
        sleep(0.05)
    return 'OK'


@app.route('/twinkle-random', methods=['PUT'])
def twinkle_random():
    print('twinkle random')
    break_running_mode()
    set_all(0, 0, 0)
    while True:
        for i in range(strip.numPixels() / 2):
            if break_mode == True:
                return
            set_pixel(random.randint(0, strip.numPixels()), random.randint(0, 255),
                      random.randint(0, 255), random.randint(0, 255))
            strip.show()
            sleep(0.1)
        set_all(0, 0, 0)


@app.route('/running-lights', methods=['PUT'])
def running_lights():
    print('running lights')
    break_running_mode()
    set_all(0, 0, 0)
    while True:
        pos = 0
        for j in range(strip.numPixels() * 2):
            if break_mode == True:
                return
            pos = pos + 1
            for i in range(strip.numPixels()):
                setPixel(i, ((math.sin(i + pos) * 127 + 128) / 255) * random.randint(0, 255),
                         ((math.sin(i + pos) * 127 + 128) / 255)
                         * random.randint(0, 255),
                         ((math.sin(i + pos) * 127 + 128) / 255) * random.randint(0, 255))
            strip.show()
            sleep(0.05)


# @app.route('/meteor-rain', methods=['PUT'])
# def meteor_rain(red=255, green=255, blue=255):
#    print('meteor rain')
#    break_running_mode()

#    while True:
#        set_all(0, 0, 0)
#        for i in range(strip.numPixels() * 2):
#            # fade brightness all LEDs one step
#            for j in range(strip.numPixels()):
#                if break_mode == True:
#                    return
#                if(random.randint(0, 10) > 5):
#                    oldColor = strip.getPixelColor(j)
#                    r = (oldColor & 0x00ff00) >> 16
#                    g = (oldColor & 0xff0000) >> 8
#                    b = (oldColor & 0x0000ff)
#
#                    if r <= 10:
#                        r = 0
#                    else:
#                        int(r - (r * 64 / 256))
#                    if g <= 10:
#                        g = 0
#                    else:
#                        g = int(g - (g * 64 / 256))
#                    if b <= 10:
#                        b = 0
#                    else:
#                        b = int(b - (b * 64 / 256))
#
#                    set_pixel(j, r, g, b)
#
# draw meteor
#            for j in range(10):
#                if((i - j < strip.numPixels()) and (i - j >= 0)):
#                    setPixel(i - j, red, green, blue)
#
#            strip.show()
#            sleep(0.03)
