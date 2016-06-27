
from logging import warning, debug, error, info
from PIL import Image, ImageColor, ImageDraw
import random

from .camera import CameraController
from .gpio import GPIOButton
from .timer import Timer
from . import ui

NAME_GET_STARTED    = "get_started"

STATE_DEFAULT           = 0
STATE_EXIT_PROMPT       = 1
STATE_PREPARE           = 2
STATE_PICTURE_COUNTDOWN = 3
STATE_PICTURE_TAKEN     = 4
STATE_PRINT             = 5
STATE_COMPLETED         = 6


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
        self.yes_button = None
        self.no_button = None
        self.fps = 1
        self.picture_count = 4

        self.state = STATE_DEFAULT
        self.render_timer = Timer(0.1)
        self.countdown_timer = Timer()
        self.pictures_taken = 0

    def _logic(self):
        """
        Called by the UI system on every tick so that it can be updated.
        :param root: the ui root
        """
        yes = self.yes_button.was_pressed or self.yes_button.pressed
        no = self.no_button.was_pressed or self.no_button.pressed

        # render
        if self.render_timer.finished:
            # start = time()
            self.window_renderer.update(self.buffer_image.tobytes())
            # debug("render time: %s", time() - start)
            self.render_timer.start()

        if self.state == STATE_DEFAULT:
            if no:
                self._enter_state(STATE_EXIT_PROMPT)
            elif yes:
                self._enter_state(STATE_PREPARE)

        elif self.state == STATE_EXIT_PROMPT:
            if yes:
                return False
            elif no:
                self._enter_state(STATE_DEFAULT)

        elif self.state == STATE_PREPARE:
            if no:
                self._enter_state(STATE_DEFAULT)
            elif self.countdown_timer.finished:
                self.pictures_taken = 0
                self._enter_state(STATE_PICTURE_COUNTDOWN)

        elif self.state == STATE_PICTURE_COUNTDOWN:
            if no:
                self._enter_state(STATE_DEFAULT)
            elif self.countdown_timer.finished:
                # TODO: TAKE PHOTO
                self._enter_state(STATE_PICTURE_TAKEN)
            else:
                self.window.find_by_name(NAME_GET_STARTED).text = "" \
                        + str(self.pictures_taken + 1) + " of " + str(self.picture_count) \
                        + "\n" + str(int(self.countdown_timer.remaining) + 1)

        elif self.state == STATE_PICTURE_TAKEN:
            if no:
                self._enter_state(STATE_DEFAULT)
            elif self.countdown_timer.finished:
                self.pictures_taken += 1
                if self.pictures_taken >= self.picture_count:
                    self._enter_state(STATE_PRINT)
                else:
                    self._enter_state(STATE_PICTURE_COUNTDOWN)

        elif self.state == STATE_PRINT:
            if no or self.countdown_timer.finished:
                self._enter_state(STATE_DEFAULT)
            elif yes:
                # TODO: RENDER AND PRINT
                self._enter_state(STATE_COMPLETED)

        elif self.state == STATE_COMPLETED:
            if yes or no or self.countdown_timer.finished:
                self._enter_state(STATE_DEFAULT)

        else:
            raise RuntimeError("The app is in an unknown state: " + str(self.state))

        return True

    def _enter_state(self, state):
        """
        Manages switching between states
        :param state: the state to switch to
        """
        debug("entering state: %s", state)

        if state == STATE_DEFAULT:
            self.pictures_taken = 0
            self.window.find_by_name(NAME_GET_STARTED).text = "Tap the button\nto get started"
            self.window.find_by_name(NAME_GET_STARTED).font_color = (0, 0, 0, 255)

        elif state == STATE_EXIT_PROMPT:
            self.window.find_by_name(NAME_GET_STARTED).text = "Exit?"
            self.window.find_by_name(NAME_GET_STARTED).font_color = (255, 0, 0, 255)

        elif state == STATE_PREPARE:
            self.window.find_by_name(NAME_GET_STARTED).text = "Ok, get ready!"
            self.window.find_by_name(NAME_GET_STARTED).font_color = (0, 0, 0, 255)
            self.countdown_timer.start(3)

        elif state == STATE_PICTURE_COUNTDOWN:
            self.window.find_by_name(NAME_GET_STARTED).font_color = (0, 0, 0, 255)
            self.countdown_timer.start(5)

        elif state == STATE_PICTURE_TAKEN:
            self.window.find_by_name(NAME_GET_STARTED).text = random.sample(ui.picture_taken_sentances, 1)[0]
            self.countdown_timer.start(3)

        elif state == STATE_PRINT:
            self.window.find_by_name(NAME_GET_STARTED).text = "Print?"
            self.countdown_timer.start(10)

        elif state == STATE_COMPLETED:
            self.window.find_by_name(NAME_GET_STARTED).text = "Thank You!"
            self.countdown_timer.start(5)

        else:
            raise RuntimeError("Attempted to enter an unknown state: " + str(state))

        self.state = state
        debug("entered state: %s", state)

    def run(self, photo_resolution, yes_pin, no_pin):
        """
        Starts the application.  This method blocks until the application is stopped.
        """

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

        info("setting up input")
        self.yes_button = GPIOButton(yes_pin)
        self.no_button = GPIOButton(no_pin)

        info("starting app")
        self._enter_state(STATE_DEFAULT)
        self.render_timer.start()
        ui_context = ui.UIContext(self.canvas, self.window, update_function=self._logic)
        ui_context.main_loop()

        info("exiting")

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
        interface_frame.background_color = ImageColor.getcolor('#ffffff', 'RGB')

        number = ui.LabelWidget("",
                                name=NAME_GET_STARTED,
                                parent=interface_frame,
                                align="center",
                                font_color=(0, 0, 0, 255))
        number.dimensions = (
            5, 5,
            interface_frame.width - 10,
            interface_frame.height - 10
        )

