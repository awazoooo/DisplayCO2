# coding: UTF-8

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import time
import mh_z19

def clear(disp):
    disp.clear()
    disp.display()

def draw(disp):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Draw a black filled box to clear the image.
    # draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Get sensor value
    with open('/root/DisplayCO2/co2_logs/log', 'r') as fp:
        temp, co2 = fp.readline().replace('\n', '').split(',')
    # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    # MemUsage = subprocess.check_output(cmd, shell = True )
    # cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    # Disk = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.
    draw.text((x, top),    "CO2 : {}ppm".format(str(co2)), font=font, fill=255)
    draw.text((x, top+10), "TEMP: {}°C".format(str(temp)),  font=font, fill=255)
    # draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    # draw.text((x, top+25),    str(Disk),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

if __name__ == '__main__':
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_address=0x3C)

    # Initialize
    disp.begin()

    # Clear display
    clear(disp)

    # Draw Display
    draw(disp)
