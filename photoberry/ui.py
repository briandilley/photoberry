
import ctypes
from logging import debug
from picamera import bcm_host, mmal


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


class Widget(object):
    """
    A renderable widget
    """

    def __init__(self, parent=None, dimensions=None):
        super(Widget, self).__init__()
        self._parent = None
        self._dimensions = (0, 0, 0, 0)
        self._visible = True
        self.children = list()
        self.background_color = None
        self.dirty = True
        if parent:
            parent.add_child(self)
        if dimensions:
            self.dimensions = dimensions

    def layout(self):
        """
        Called whenever the wiget's dimensions change.
        """
        pass

    def add_child(self, child):
        """
        Adds a child widget
        :param child: the child to add
        """
        self.children.append(child)
        child.parent = self
        self.dirty = True

    def remove_child(self, child):
        """
        Removes a child widget.  Raises ValueError if the child was not present
        :param child: the child to remove
        """
        self.children.remove(child)
        child.parent = None
        self.dirty = True

    def draw(self, canvas):
        """
        An :class:`~ImageDraw` class is passed as a canvas for the widget to draw itself.
        :param canvas: the canvas
        """
        if not self.visible:
            return
        if self.background_color:
            debug("drawing: %s", self.screen_dimensions)
            canvas.rectangle((
                self.screen_dimensions[0],
                self.screen_dimensions[1],
                self.screen_dimensions[0] + self.screen_dimensions[2],
                self.screen_dimensions[1] + self.screen_dimensions[3]
            ), fill=self.background_color)
        for child in self.children:
            child.draw(canvas)
        self.dirty = False

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        if self._visible == visible:
            return
        self._visible = visible
        self.dirty = True

    @property
    def parent(self):
        """
        The Widget's parent
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent == parent:
            return
        self._parent = parent
        self.dirty = True

    @property
    def dimensions(self):
        """
        The coordinates of the widget relative to it's parent in (x,y,width,height)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        dimensions = (int(dimensions[0]), int(dimensions[1]), int(dimensions[2]), int(dimensions[3]))
        if self._dimensions == dimensions:
            return
        self._dimensions = dimensions
        self.layout()
        self.dirty = True

    @property
    def screen_dimensions(self):
        """
        The coordinates of the widget relative to the root widget in (x,y,width,height)
        """
        if not self.parent:
            return self.dimensions

        return (
            self.dimensions[0] + self.parent.screen_x,
            self.dimensions[1] + self.parent.screen_y,
            self.dimensions[2],
            self.dimensions[3]
        )

    @screen_dimensions.setter
    def screen_dimensions(self, dimensions):
        if not self.parent:
            self.dimensions = dimensions
            return
        self.dimensions = (
            int(dimensions[0]) - self.parent.screen_x,
            int(dimensions[1]) - self.parent.screen_y,
            int(dimensions[2]),
            int(dimensions[3]))

    @property
    def size(self):
        """
        The size of the widget in (width,height)
        """
        return self.dimensions[2], self.dimensions[3]

    @size.setter
    def size(self, size):
        self.dimensions = (self.x, self.y, size[0], size[1])

    @property
    def location(self):
        """
        The location of the widget in (x,y)
        """
        return self.dimensions[0], self.dimensions[1]

    @property
    def screen_location(self):
        """
        The location of the widget relative to the root widget in (x,y)
        """
        if not self.parent:
            return self.location

        return (
            self.location[0] + self.parent.screen_location,
            self.location[1] + self.parent.screen_location
        )

    @location.setter
    def location(self, location):
        self.dimensions = (location[0], location[1], self.width, self.height)

    @property
    def x(self):
        """
        The `x` coordinate of the widget relative to it's parent
        """
        return self.dimensions[0]

    @property
    def screen_x(self):
        """
        The `x` coordinate of the widget relative to the root widget
        """
        if not self.parent:
            return self.x
        return self.x + self.parent.screen_x

    @x.setter
    def x(self, x):
        self.dimensions = (
            x,
            self.dimensions[1],
            self.dimensions[2],
            self.dimensions[3])

    @property
    def y(self):
        return self.dimensions[1]

    @property
    def screen_y(self):
        """
        The `y` coordinate of the widget relative to the root widget
        """
        if not self.parent:
            return self.y
        return self.y + self.parent.screen_y

    @y.setter
    def y(self, y):
        """
        The `y` coordinate of the widget
        """
        self.dimensions = (
            self.dimensions[0],
            y,
            self.dimensions[2],
            self.dimensions[3])

    @property
    def width(self):
        """
        The `width` of the widget
        """
        return self.dimensions[2]

    @width.setter
    def width(self, width):
        self.dimensions = (
            self.dimensions[0],
            self.dimensions[1],
            width,
            self.dimensions[3])

    @property
    def height(self):
        """
        The `height` of the widget
        """
        return self.dimensions[3]

    @height.setter
    def height(self, height):
        self.dimensions = (
            self.dimensions[0],
            self.dimensions[1],
            self.dimensions[2],
            height)
