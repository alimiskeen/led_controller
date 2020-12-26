#!/usr/bin/env python3
import board
import neopixel
import threading
import colorify
import time

# global values
ORDER = neopixel.GRB
pixel_pin = board.D18
num_pixels = (150 * 18)


def delegate_format(pixel: neopixel.NeoPixel, input_item: any) -> None:
    item = input_item[0]
    pixel.fill((100, 100, 100))


def color_wheel(pixel: neopixel.NeoPixel, input_item: colorify.Color) -> None:
    c = input_item
    pixel.fill(c.get_rgb())
    c.change_hue(1)


def eclipse_equation(x: int, y: int) -> bool:
    left = ((x - 75) ** 2) / (50 ** 2)
    right = ((x - 18) ** 2) / (8 ** 2)
    return (left + right) < 1


def lightup_desk(pixel: neopixel.NeoPixel, input_item: None) -> None:
    for y in range(18):
        for x in range(150):
            if eclipse_equation(x, y):
                print("in eclipse")
                pixel[xy_to_index(x, y)] = (100, 100, 100)


def test_position(pixel: neopixel.NeoPixel, input_item: None) -> None:
    positions = [(pos_x, pos_y) for pos_x in [0, 75] for pos_y in range(18)]
    for x, y in positions:
        pixel[xy_to_index(x, y)] = (255, 255, 255)


def xy_to_index(x: int, y: int) -> int:
    """

    :param x: position of the led in the x direction
    :param y: position of the led in the y direction
    :return: the index of the led in the neopixel object
    :raises ValueError: when one of the inputs is negative
    """
    if x < 0 or y < 0:
        raise IndexError("cannot have a negative input")
    index = y * 150
    if y % 2 == 0:
        index += x + 1
    else:
        index += (150 - x) + 1
    return index


class Screen:

    def __init__(self, num_of_pixels, pin, drawing_method=delegate_format, drawing_variable=None, brightness=0.5):
        if drawing_variable is None:
            drawing_variable = [0]
        self.pixels = neopixel.NeoPixel(pin, num_of_pixels, auto_write=False, brightness=brightness)
        self.drawing_method = drawing_method
        self.drawing_variable = drawing_variable

    def _draw(self):
        while True:  # TODO: implement timing for frame drawing
            self.drawing_method(self.pixels, self.drawing_variable)
            self.pixels.show()  # TODO: try to maybe use a delegate per frame instead of a delegate per led
            # time.sleep(33 / 1000)  # TODO: fix the timing, from rigid to remaining time to next frame

    def main_loop(self):
        thr = threading.Thread(target=self._draw)
        thr.start()

    def change_method(self, method):
        self.drawing_method = method


if __name__ == '__main__':
    # something
    print("display has started, CTRL C to stop")
    col = colorify.Color(255, 10, 10)
    # screen = Screen(num_pixels, pixel_pin, drawing_method=color_wheel, drawing_variable=col)
    screen = Screen(num_pixels, pixel_pin, drawing_method=test_position)
    screen.main_loop()
