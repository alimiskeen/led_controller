#!/usr/bin/env python3

# import neopixel
# import board

# pixels = neopixel.NeoPixel(18, 30, auto_write=False)
#
# pixels[0] = (255, 0, 0)
#
# pixels.brightness = .9
#
# pixels.show()

# print(dir(board))
import math
import colorsys


def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v


class Color:

    def __init__(self, r, b, g):
        self._Red = r
        self._Blue = b
        self._Green = g
        self._Hue, self._Saturation, self._Value = colorsys.rgb_to_hsv(r, g, b)

    def change_hue(self, hue):
        self._Hue = self._Hue + math.radians(hue)
        if self._Hue > 2*math.pi:
            self._Hue = 0
        self._Red, self._Green, self._Blue = colorsys.hsv_to_rgb(self._Hue, self._Saturation, self._Value)
        self._Red = int(self._Red)
        self._Green = int(self._Green)
        self._Blue = int(self._Blue)

    def get_rgb(self):
        return self._Red, self._Blue, self._Green

    def __str__(self):
        return f'({self._Red},{self._Blue},{self._Green}) or ({self._Hue},{self._Saturation},{self._Value})'


if __name__ == '__main__':

    c = Color(255, 50, 120)
    print(c)
    c.change_hue(180)
    print(c)

