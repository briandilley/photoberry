
from time import time


class Timer(object):

    def __init__(self, duration=0):
        self._duration = duration
        self._start = 0

    def start(self, duration=None):
        if duration:
            self._duration = duration
        self._start = time()

    def stop(self):
        self._start = 0

    @property
    def remaining(self):
        return self._duration - (time() - self._start)

    @property
    def finished(self):
        return self.remaining <= 0

    @property
    def started(self):
        return self._start > 0

