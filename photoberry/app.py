
from .camera import CameraController


class PhotoBerryApplication(object):

    def __init__(self):
        self.camera_controller = None

    def run(self):
        self.camera_controller = CameraController()



