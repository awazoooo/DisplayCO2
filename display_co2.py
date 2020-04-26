# coding: UTF-8

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import time
import datetime
import mh_z19

def getCO2():
    # root authority required
    dat = mh_z19.read_all()
    return dat['co2'], dat['temperature']

def draw_display(disp, gpio_interval=5):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    #draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    while True:
        # Get CO2 sensor.
        co2, temp = getCO2()
        dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        # GPIO interval.
        time.sleep(gpio_interval)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        draw.text((x, top), "{}".format(dt),  font=font, fill=255)
        # Set sensor data.
        draw.text((x, top+15), "CO2 : {}ppm".format(str(co2)), font=font, fill=255)
        draw.text((x, top+25), "TEMP: {}°C".format(str(temp)),  font=font, fill=255)


        # Display image.
        disp.image(image)
        disp.display()

        # GPIO interval time.
        time.sleep(gpio_interval)

def init_display():
    # Get display object.
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_address=0x3C)

    # Init display.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()
    return disp

if __name__ == '__main__':
    # Initialize display.
    disp = init_display()

    # Infinite loop.
    draw_display(disp, 0.5)
