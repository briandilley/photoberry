
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class GPIOButton(object):
    """
    A simple button that uses GPIO
    """

    def __init__(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._gpio_event)
        self._pin = pin
        self._pressed = False
        self._was_pressed = False
        self._was_released = False

    def _gpio_event(self, pin):
        if pin != self._pin:
            return
        self._was_pressed = self.pressed
        self._was_released = not self._was_pressed

    @property
    def was_pressed(self):
        """
        Checks as to whether or not the button was released, also
        clearing the flag if it was in fact released.
        :return: True if released, False otherwise
        """
        ret = self._was_released
        self._was_pressed = False
        self._was_released = False
        return ret

    @property
    def was_pressed(self):
        """
        Checks as to whether or not the button was pressed, also
        clearing the flag if it was in fact pressed.
        :return: True if pressed, False otherwise
        """
        ret = self._was_pressed
        self._was_pressed = False
        self._was_released = False
        return ret

    @property
    def pressed(self):
        return GPIO.input(self._pin) == False

