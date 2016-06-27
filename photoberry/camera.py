
import os
import picamera
from shutil import rmtree
from tempfile import mkstemp, mkdtemp

from time import sleep


class CameraController(object):

    def __init__(self):
        self._camera = None
        self.preview_renderer = None
        self.camera = picamera.PiCamera()
        self.work_dir = None
        self.clear_workdir()

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
        :param source: the source
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

    def clear_workdir(self):
        """
        Deletes all files in the working directory
        """
        if self.work_dir and os.path.exists(self.work_dir):
            rmtree(self.work_dir, ignore_errors=True)
        self.work_dir = mkdtemp('work', 'photoberry')
        return self.work_dir

    def capture_photo(self):
        """
        Captures a photo to a temporary file in the working directory
        :return: the file
        """
        (handle, file_name) = mkstemp(suffix='.jpg', prefix='photoberry-temp', dir=self.work_dir)
        os.close(handle)
        handle = open(file_name, 'wb')
        self.camera.capture(handle, format='jpeg', quality=100)
        handle.close()
        return file_name
