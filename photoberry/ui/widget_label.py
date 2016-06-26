
from logging import debug, error
import os
from PIL import ImageFont

from . import Widget

assets_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),  "../assets")
fonts_dir = os.path.join(assets_dir, "fonts")
default_font = os.path.join(fonts_dir, "Roboto-Medium.ttf")


class LabelWidget(Widget):
    """
    A widget for rendering text
    """

    def __init__(self, text,
                 font_name=default_font,
                 font_color=(255, 0, 0, 255),
                 align="left",
                 parent=None,
                 dimensions=None):
        super(LabelWidget, self).__init__(parent=parent, dimensions=dimensions)
        self._text = text
        self._font_name = font_name
        self._align = align
        self._font_color = font_color
        self._font_size = -1
        self._font = None
        self._box_size = None

    def _find_font_size(self, canvas):
        font_size = 1
        font = ImageFont.truetype(self.font_name, font_size)
        box_size = canvas.textsize(self.text, font=font)
        while True:
            new_font = ImageFont.truetype(self.font_name, font_size)
            new_box_size = canvas.textsize(self.text, font=new_font)
            if new_box_size[0] > self.width or new_box_size[1] > self.height:
                break
            font_size += 1
            font = new_font
            box_size = new_box_size

        self._font_size = font_size
        self._font = font
        self._box_size = box_size

    def do_draw(self, canvas):
        if self._font_size == -1:
            self._find_font_size(canvas)
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
        self._font_size = -1

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
        self._font_size = -1

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align):
        self._align = align

