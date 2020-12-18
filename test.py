#!/usr/bin/env python3

import neopixel
import board

pixels = neopixel.NeoPixel(board.D18, 30, auto_write=False)

pixels[0] = (255, 0, 0)

pixels.brightness = .9

pixels.show()

print(dir(board))



