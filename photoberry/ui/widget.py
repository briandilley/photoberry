
class Widget(object):
    """
    A renderable widget
    """

    def __init__(self, name=None, parent=None, dimensions=None):
        super(Widget, self).__init__()
        self._parent = None
        self._dimensions = (0, 0, 0, 0)
        self._visible = True
        self._dirty = True
        self.name = name
        self.children = list()
        self.background_color = None
        if parent:
            parent.add_child(self)
        if dimensions:
            self.dimensions = dimensions

    def do_layout(self, canvas):
        """
        To be overridden by subclasses to lay themselves out
        :param canvas: the canvas
        """
        pass

    def do_draw(self, canvas):
        """
        To be overridden by subclasses to draw themselves
        :param canvas: the canvas
        """
        pass

    def layout(self, canvas):
        """
        Called when the widget needs to lay itself out
        """
        if not self.visible:
            return
        self.do_layout(canvas)
        self._dirty = False
        for child in self.children:
            child.layout(canvas)

    def find_by_name(self, name):
        """
        Finds a widget by name.
        :param name: the name
        :return: the widget, or None if not found
        """
        if self.name == name:
            return self
        for child in self.children:
            if child.name == name:
                return child
        for child in self.children:
            ret = child.find_by_name(name)
            if ret:
                return ret
        return None

    def draw(self, canvas):
        """
        An :class:`~ImageDraw` class is passed as a canvas for the widget to draw itself.
        :param canvas: the canvas
        """
        if not self.visible:
            return
        if self.background_color:
            canvas.rectangle((
                self.screen_dimensions[0],
                self.screen_dimensions[1],
                self.screen_dimensions[0] + self.screen_dimensions[2],
                self.screen_dimensions[1] + self.screen_dimensions[3]
            ), fill=self.background_color)
        self.do_draw(canvas)
        for child in self.children:
            child.draw(canvas)

    def invalidate(self):
        """
        Marks this widget as invalid which causes it to be re layed out and drawn.
        """
        self._dirty = True

    def add_child(self, child):
        """
        Adds a child widget
        :param child: the child to add
        """
        self.children.append(child)
        child.parent = self
        self.invalidate()

    def remove_child(self, child):
        """
        Removes a child widget.  Raises ValueError if the child was not present
        :param child: the child to remove
        """
        self.children.remove(child)
        child.parent = None
        self.invalidate()

    @property
    def dirty(self):
        """
        Indicates whether or not this widget has been invalidated and is considered
        to be a dirty, dirty... dirty little girl.
        :return: True if invalid
        """
        if self._dirty:
            return True
        for child in self.children:
            if child.dirty:
                return True
        return False

    @property
    def root(self):
        """
        Returns the root widget in this widget's hierarchy.
        :return: the root widget
        """
        return self.root if self.parent else self

    @property
    def visible(self):
        """
        Indicates wheter or not this widget is visible.
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        """
        Sets this widget's visibility
        :param visible: the visibility
        """
        if self._visible == visible:
            return
        self._visible = visible
        self.invalidate()

    @property
    def name(self):
        """
        The Widget's name
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the widget's name
        :param parent: the name
        """
        self._name = name

    @property
    def parent(self):
        """
        The Widget's parent
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the widget's parent
        :param parent: the parent
        """
        if self._parent == parent:
            return
        self._parent = parent
        self.invalidate()

    @property
    def dimensions(self):
        """
        The coordinates of the widget relative to it's parent in (x,y,width,height)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the widgets dimensions.
        :param dimensions: the dimensions
        """
        dimensions = (int(dimensions[0]), int(dimensions[1]), int(dimensions[2]), int(dimensions[3]))
        if self._dimensions == dimensions:
            return
        self._dimensions = dimensions
        self.invalidate()

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
        """
        Sets the widget's dimensions using the screen dimensions.
        :param dimensions: the dimensions
        """
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
        """
        Sets thew size (width, height) of the widget
        :param size:  the size
        """
        self.dimensions = (self.x, self.y, size[0], size[1])
        self.invalidate()

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
            self.location[0] + self.parent.screen_location[0],
            self.location[1] + self.parent.screen_location[1]
        )

    @location.setter
    def location(self, location):
        """
        Sets the location of the widget (x, y)
        :param location: the location
        """
        self.dimensions = (location[0], location[1], self.width, self.height)
        self.invalidate()

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
        """
        Sets the x coordinate of the widget
        :param x: the x
        """
        self.dimensions = (
            x,
            self.dimensions[1],
            self.dimensions[2],
            self.dimensions[3])
        self.invalidate()

    @property
    def y(self):
        """
        The `y` coordinate of the widget
        """
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
        self.invalidate()

    @property
    def width(self):
        """
        The `width` of the widget
        """
        return self.dimensions[2]

    @width.setter
    def width(self, width):
        """
        Sets the `width` of the widget
        """
        self.dimensions = (
            self.dimensions[0],
            self.dimensions[1],
            width,
            self.dimensions[3])
        self.invalidate()

    @property
    def height(self):
        """
        The `height` of the widget
        """
        return self.dimensions[3]

    @height.setter
    def height(self, height):
        """
        Sets the `height` of the widget
        """
        self.dimensions = (
            self.dimensions[0],
            self.dimensions[1],
            self.dimensions[2],
            height)
        self.invalidate()
