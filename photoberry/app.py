
from logging import warning, debug, error, info
from PIL import Image, ImageColor, ImageDraw
from time import sleep

from .camera import CameraController
from . import ui


class PhotoBerryApplication(object):
    """The application object is"""

    def __init__(self):
        self.camera_controller = None
        self.window = None
        self.window_renderer = None
        self.preview_renderer = None
        self.buffer_image = None
        self.canvas = None
        self.screen_resolution = None
        self.normalized_screen_resolution = None

    def run(self, photo_resolution, fps=1):
        """
        Starts the application.  This method blocks until the application is stopped.
        """

        warning("warning")
        debug("debug")
        error("error")
        info("info")

        info("creating camera")
        self.camera_controller = CameraController()
        self.camera_controller.camera.resolution = photo_resolution

        self.screen_resolution = ui.get_screen_resolution()
        self.normalized_screen_resolution = ui.normalize_dimension(self.screen_resolution)
        info("screen_resolution: %s", self.screen_resolution)
        info("normalized_screen_resolution: %s", self.normalized_screen_resolution)

        info("creating buffer image and canvas")
        self.buffer_image = Image.new('RGB', self.normalized_screen_resolution)
        self.canvas = ImageDraw.Draw(self.buffer_image)
        debug("buffer_image resolution: %s", self.buffer_image.size)

        info("creating preview renderer")
        self.preview_renderer = self.camera_controller.start_preview(
            fullscreen=False,
            window=ui.normalize_dimension((
                0, 0,
                self.normalized_screen_resolution[0] * 0.75,
                self.normalized_screen_resolution[1]
            )))
        debug("preview location: %s", self.preview_renderer.window)

        info("creating window renderer")
        self.window_renderer = self.camera_controller.add_overlay(
            self.buffer_image.tobytes(),
            size=self.buffer_image.size,
            fullscreen=False,
            layer=1,
            window=(
                0, 0,
                self.normalized_screen_resolution[0],
                self.normalized_screen_resolution[1]
            ))
        debug("window location: %s", self.window_renderer.window)

        info("setting up UI")
        self._setup_ui()

        while True:
            self.window.draw(self.canvas)
            self.window_renderer.update(self.buffer_image.tobytes())
            sleep(2 / fps)

    def _setup_ui(self):
        """
        Sets up the UI
        """

        self.window = ui.Widget()
        self.window.dimensions = ui.normalize_dimension((
            0, 0,
            self.normalized_screen_resolution[0],
            self.normalized_screen_resolution[1]
        ))
        self.window.background_color = ImageColor.getcolor('#000000', 'RGB')

        interface_frame = ui.Widget(parent=self.window)
        interface_frame.dimensions = ui.normalize_dimension((
            self.preview_renderer.window[2],
            0,
            self.normalized_screen_resolution[0] - self.preview_renderer.window[2],
            self.normalized_screen_resolution[1]
        ))
        interface_frame.background_color = ImageColor.getcolor('#0000ff', 'RGB')

