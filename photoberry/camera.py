
import io


class CameraController(object):

    def __init__(self):
        self._camera = None

    def __getattribute__(self, name):

        if name == 'camera':
            if not self._camera:
                import picamera
                self._camera = picamera.PiCamera()
            return self._camera
        else:
            return object.__getattribute__(self, name)

    def read_photo_frame(self, stream=None):
        if not stream:
            stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg', resize=(640, 360))
        return stream
