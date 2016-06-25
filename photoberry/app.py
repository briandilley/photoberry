
from time import sleep
from PIL import Image

from .camera import CameraController


class PhotoBerryApplication(object):

    def __init__(self):
        self.camera_controller = None
        self.preview_resolution = None
        self.ui_overlay = None

    def run(self):

        self.camera_controller = CameraController()

        if self.preview_resolution:
            self.camera_controller.camera.resolution = self.preview_resolution

        self.camera_controller.camera.start_preview()
        if not self.preview_resolution:
            self.preview_resolution = self.camera_controller.camera.preview.resolution

        self.ui_overlay = Image.new('RGB', (
                ((((self.preview_resolution[0] / 2) + 31) // 32) * 32),
                ((((self.preview_resolution[1] / 2) + 15) // 16) * 16)
            ))

        print(str((
            (self.preview_resolution[0] / 2),
            (self.preview_resolution[1] / 2)
        )))

        o = self.camera_controller.camera.add_overlay(self.ui_overlay.tobytes(), size=self.ui_overlay.size, fullscreen=False, window=(100, 100, 200, 200))
        o.layer = 3

        while True:
            sleep(1)


