
import ctypes
from picamera import bcm_host, mmal

from .widget import Widget
from .widget_label import LabelWidget


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

