#!/usr/bin/env python3

import neopixel
import board

pixels = neopixel.NeoPixel(board.D18, 30)

pixels[0] = (255, 0, 0)

print(dir(board))



