
import io
import picamera

from time import sleep

class CameraController(object):

    def __init__(self):
        self._camera = None
        self.preview_renderer = None
        self.camera = picamera.PiCamera()

    def start_preview(self, **options):
        """
        Starts the preview.
        :param options: See :meth:`~picamera.camera.PiCamera.start_preview`
        """

        self.preview_renderer = self.camera.start_preview(**options)

        wait = 0
        while True:
            if self.preview_renderer.window[2] > 0:
                break
            wait += 1
            if wait > 10:
                raise RuntimeError('Waited longer than 10 seconds for preview window')
            sleep(1)

        return self.preview_renderer

    def add_overlay(self, source, size=None, **options):
        """
        Adds an overlay
        :param options: See :meth:`~picamera.camera.PiCamera.add_overlay`
        :param size: See :meth:`~picamera.camera.PiCamera.add_overlay`
        """

        overlay = self.camera.add_overlay(source, size=size, **options)

        wait = 0
        while True:
            if overlay.window[2] > 0:
                break
            wait += 1
            if wait > 10:
                raise RuntimeError('Waited longer than 10 seconds for overlay window')
            sleep(1)

        return overlay

    def read_photo_frame(self, stream=None):
        """
        Reads an image from the camera.  The data can be written to the stream
        provided, or a new stream is created and returnd.

        :param stream: An optional :class:BytesIO to write the image data to.
        :return: a :class:`~BytesIO`
        """

        if not stream:
            stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg', resize=(640, 360))
        return stream
