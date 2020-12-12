# coding: UTF-8

import Adafruit_SSD1306
import time
import datetime
import mh_z19
import requests
import toml
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getCO2():
    # root authority required
    dat = mh_z19.read_all()
    return dat['co2'], dat['temperature']


def draw_display(disp, config):
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

    # last webhook datetime
    last_webhook_datetime = None

    while True:
        # Get CO2 sensor.
        co2, temp = getCO2()
        dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        draw.text((x, top), "{}".format(dt),  font=font, fill=255)
        # Set sensor data.
        draw.text((x, top+15), "CO2 : {}ppm".format(str(co2)), font=font, fill=255)
        draw.text((x, top+25), "TEMP: {}°C".format(str(temp)),  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()

        # CO2 alert notification
        if co2 >= config['general']['co2_threshold']:
            if last_webhook_datetime is None or last_webhook_datetime + datetime.timedelta(minutes=config['general']['webhook_interval_minutes']) < datetime.datetime.now():
                data = {
                    'value1': co2,
                    'value2': temp,
                    'value3': dt
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                # Webhook
                r = requests.post(
                    url = config['general']['webhook_url'],
                    json = data,
                    headers = headers
                )
                print(r.text)
                last_webhook_datetime = datetime.datetime.now()

        # GPIO interval time.
        time.sleep(config['general']['co2_measure_interval_seconds'])


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

    # Read toml config file.
    config = toml.load(open('config.toml'))

    # Infinite loop.
    draw_display(disp, config)
