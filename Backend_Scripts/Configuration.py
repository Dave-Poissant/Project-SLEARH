
from Mode import Mode

class Configuration:

    def __init__(self):
        self._available_chars = ["a", "b"]
        self._mode = Mode.standard
        self._semi_auto = False

    def get_available_chars(self):
        return self._available_chars

    def toggle_semi_auto(self):
        self._semi_auto = not self._semi_auto

    def is_semi_auto(self):
        return self._semi_auto

    def set_mode(self, mode):
        self._mode = mode

    def get_mode(self):
        return self._mode

Instance = Configuration()