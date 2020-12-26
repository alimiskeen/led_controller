#!/usr/bin/env python3
import board
import neopixel
import threading
import time


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


def basic_color_wheel(x: int, y: int, inputs: list) -> tuple:
    if inputs[0] < 10000:
        inputs[0] += 1
        return 255, 0, 0
    elif inputs[0] < 20000:
        inputs[0] += 1
        return 0, 255, 0
    elif inputs[0] < 30000:
        inputs[0] += 1
        return 0, 0, 255
    else:
        inputs[0] = 0
        return 255, 0, 0


class AliPixel:

    def __init__(self, drawing_method=basic_color_wheel, drawing_variable=[0]):
        self.pixels = neopixel.NeoPixel(board.D18, (150 * 18 + 10), auto_write=False)
        self.drawing_method = drawing_method
        self.drawing_variable = drawing_variable

    def _draw(self):
        if self.drawing_method is None:
            raise Exception(" can't draw without an external drawing method")

        while True:  # TODO: implement timing for frame drawing
            for y in range(19):
                for x in range(150):
                    self.pixels[xy_to_index(x, y)] = self.drawing_method(x, y, self.drawing_variable)
            self.pixels.show()  # TODO: try to maybe use a delegate per frame instead of a delegate per led
            time.sleep(33 / 1000)  # TODO: fix the timing, from rigid to remaining time to next frame

    def main_loop(self):
        thr = threading.Thread(target=self._draw)
        thr.start()


if __name__ == '__main__':
    print("starting threaded pixel display")
    screen = AliPixel()
    screen.main_loop()
