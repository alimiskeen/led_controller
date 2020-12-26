#!/usr/bin/env python3
import board
import neopixel
import threading
import time

# global values
ORDER = neopixel.GRB
pixel_pin = board.D18
num_pixels = (150 * 18)


def delegate_format(self: neopixel.NeoPixel, input_list: list) -> None:
    item = input_list[0]
    self.fill((100, 100, 100))


def eclipse_equation(x: int, y: int) -> bool:
    left = ((x - 75) ** 2) / (50 ** 2)
    right = ((x - 18) ** 2) / (8 ** 2)
    return (left + right) < 1


def lightup_desk(self: neopixel.NeoPixel, input_list: list) -> None:
    for y in range(18):
        for x in range(150):
            if eclipse_equation(x, y):
                print("in eclipse")
                self[xy_to_index(x, y)] = (100, 100, 100)


def xy_to_index(x: int, y: int) -> int:
    """

    :param x: position of the led in the x direction
    :param y: position of the led in the y direction
    :return: the index of the led in the neopixel object
    :raises ValueError: when one of the inputs is negative
    """
    if x < 0 or y < 0:
        raise ValueError("cannot have a negative input")
    index = y * 150
    index += x + 1
    return index


class Screen:

    def __init__(self, num_of_pixels, pin, drawing_method=delegate_format, drawing_variable=None):
        if drawing_variable is None:
            drawing_variable = [0]
        self.pixels = neopixel.NeoPixel(pin, num_of_pixels, auto_write=False)
        neopixel.NeoPixel.drawing_method = drawing_method
        self.drawing_variable = drawing_variable

    def _draw(self):
        while True:  # TODO: implement timing for frame drawing
            self.pixels.drawing_method(self.drawing_variable)
            self.pixels.show()  # TODO: try to maybe use a delegate per frame instead of a delegate per led
            # time.sleep(33 / 1000)  # TODO: fix the timing, from rigid to remaining time to next frame

    def main_loop(self):
        thr = threading.Thread(target=self._draw)
        thr.start()

    def change_method(self, method):
        neopixel.NeoPixel.drawing_method = method


if __name__ == '__main__':
    print("starting threaded pixel display")
    screen = Screen(num_pixels, pixel_pin, drawing_method=lightup_desk)
    screen.main_loop()
