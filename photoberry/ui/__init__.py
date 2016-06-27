import ctypes
from time import sleep, time
from logging import debug
from picamera import bcm_host, mmal

from .widget import Widget
from .widget_label import LabelWidget
from .constants import *


class UIContext(object):
    """
    Does the main loop for the UI
    """

    def __init__(self, canvas, root, update_function=lambda x: 0):
        self._canvas = canvas
        self._update_function = update_function
        self._root = root

    def main_loop(self):
        while self._update_function():
            if self._root.dirty:

                # start = time()
                self._root.layout(self._canvas)
                # debug("layout time: %s", time() - start)

                # start = time()
                self._root.draw(self._canvas)
                # debug("draw time: %s", time() - start)

            sleep(0.06)


def normalize_dimension(dimension):
    """
    Normalizes a dimension so that it's width is a multiple of 32 and
    it's height is a multiple of 16.
    :param dimension:
    :return:
    """
    if len(dimension) == 4:
        return (
            int(dimension[0]),
            int(dimension[1]),
            mmal.VCOS_ALIGN_UP(int(dimension[2]), 32),
            mmal.VCOS_ALIGN_UP(int(dimension[3]), 16)
        )
    else:
        return (
            mmal.VCOS_ALIGN_UP(int(dimension[0]), 32),
            mmal.VCOS_ALIGN_UP(int(dimension[1]), 16)
        )


def get_screen_resolution():
    """
    Returns the screen's resolution in (width, height)
    :return: the resultion
    """
    w = ctypes.c_uint32()
    h = ctypes.c_uint32()
    if bcm_host.graphics_get_display_size(0, w, h) == -1:
        w = 1280
        h = 720
    else:
        w = int(w.value)
        h = int(h.value)
    return w, h

