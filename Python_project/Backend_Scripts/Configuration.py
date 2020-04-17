from Backend_Scripts import Logger
from Backend_Scripts import EventHandler
from Backend_Scripts import Purpose


class Configuration:

    def __init__(self):
        self._available_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                                 "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        self._purpose = Purpose.Purpose.Education
        self._semi_auto = False
        self._wait_time = 2  # seconds - Wait time between letter exectition
        self.debug = False
        self.debug_level = 1

    def set_debug(self, _bool, _level):
        self.debug = _bool
        self.debug_level = _level

    def get_wait_time(self):
        return self._wait_time

    def set_wait_time(self, time):
        self._wait_time = time

    def get_available_chars(self):
        return self._available_chars

    def toggle_semi_auto(self):
        self._semi_auto = not self._semi_auto
        EventHandler.Instance.trigger = not self._semi_auto
        Logger.Log("Semi auto: " + str(self._semi_auto) + "\n", 1)

    def is_semi_auto(self):
        return self._semi_auto

    def set_purpose(self, purpose):
        self._purpose = purpose

    def get_purpose(self):
        return self._purpose

    def get_purpose_string(self):
        if self.get_purpose() == Purpose.Purpose.Education:
            return "educ"
        elif self.get_purpose() == Purpose.Purpose.Quiz:
            return "quiz"


Instance = Configuration()
