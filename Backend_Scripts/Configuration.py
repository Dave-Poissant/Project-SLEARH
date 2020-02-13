
from Mode import Mode

class Configuration:

    def __init__(self):
        self._available_chars = ["a", "b"]
        self._mode = Mode.standard
        self._semi_auto = False
        self._wait_time = 2 #seconds - Wait time between letter exectition

    def get_wait_time(self):
        return self._wait_time

    def set_wait_time(self, time):
        if type(int) == type(time):
            self._wait_time = time

    def get_available_chars(self):
        return self._available_chars

    def toggle_semi_auto(self):
        self._semi_auto = not self._semi_auto
        print("Semi auto: " + str(self._semi_auto))

    def is_semi_auto(self):
        return self._semi_auto

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

Instance = Configuration()