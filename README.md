# OctoPrint-Arduino-Neopixel

Control a NeoPixel strand from Arduino for OctoPrint.


## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually through pip using this URL:

    https://github.com/mhar9000/OctoPrint-Arduino-NeoPixel/archive/master.zip

Note: This plugin isn't yet registered in the OctoPrint plugin manager, but it should be registered soon.

## Configuration

This plugin allows you to control a AdaFruit [NeoPixel](https://www.adafruit.com/category/168) strand from an [Arduino](https://www.arduino.cc). For information on how to begin using AdaFruit NeoPixels, refer to [this](https://learn.adafruit.com/adafruit-neopixel-uberguide) guide. Then upload [this](Arduino-NeoPixel-Program.ino) code to your Arduino. It receives all of the hexadecimal codes sent by the plugin and turns the strand that color. You're welcome to modify it or replace it all together, the plugin send codes in a format like this '''<#FFFFFF>'''

This plugin also changes the color of the strand whenever a specific OctoPrint event happens, such as a printer connect or disconnected, a print start, fail, pause, and more. You can set the NeoPixel strand to change to a color you can pick from the OctoPrint settings.
