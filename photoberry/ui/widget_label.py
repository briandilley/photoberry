
from logging import debug
from PIL import ImageFont

from .widget import Widget
from .constants import default_font


class LabelWidget(Widget):
    """
    A widget for rendering text
    """

    def __init__(self, text,
                 font_name=default_font,
                 font_color=(0, 0, 0, 255),
                 align="left",
                 name=None,
                 parent=None,
                 dimensions=None):
        super(LabelWidget, self).__init__(name=name, parent=parent, dimensions=dimensions)
        self._text = text
        self._font_name = font_name
        self._align = align
        self._font_color = font_color
        self._font_size = -1
        self._font = None
        self._box_size = None

    def do_layout(self, canvas):
        min = 1
        max = 1024
        current = -1
        while min != max:
            current = min + (max - min) / 2
            if current == min or current == max:
                break
            font = ImageFont.truetype(self.font_name, current)
            box_size = canvas.textsize(self.text, font=font)
            if box_size[0] > self.width or box_size[1] > self.height:
                max = current
            else:
                min = current

        self._font_size = current
        self._font = ImageFont.truetype(self.font_name, self._font_size)
        self._box_size = canvas.textsize(self.text, font=self._font)

    def do_draw(self, canvas):
        canvas.text((
                self.screen_x + ((self.width / 2) - (self._box_size[0] / 2)),
                self.screen_y + ((self.height / 2) - (self._box_size[1] / 2))
            ), self.text, font=self._font, fill=self._font_color, align=self._align)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text == self._text:
            return
        self._text = text
        self.invalidate()

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, font_color):
        if font_color == self.font_color:
            return
        self._font_color = font_color
        self.invalidate()

    @property
    def font_name(self):
        return self._font_name

    @font_name.setter
    def font_name(self, font_name):
        if not font_name:
            raise AttributeError('font_name must not be empty')
        elif font_name == self._font_name:
            return
        self._font_name = font_name
        self.invalidate()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size
        self.invalidate()

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align):
        self._align = align
        self.invalidate()

