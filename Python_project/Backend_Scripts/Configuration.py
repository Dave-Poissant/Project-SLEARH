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
        self._debug = False
        self._debug_level = 1

    ##Method that sets the debug level to print more or less logged messages
    #@param _bool Boolean to activate (True) or desactivate (False) logged messages
    #@param _level Int Sets the maximum level of debug needed for logged meesages to be printed
    #
    def set_debug(self, _bool, _level):
        self._debug = _bool
        self._debug_level = _level

    ##Method that returns the current debug state (Boolean)
    #
    def get_debug_state(self):
        return self._debug

    ##Method that returns the current debug level (Int)
    #
    def get_debug_level(self):
        return self._debug_level

    ##Method that returns the current wait_time between letter execution in automatic mode
    #
    def get_wait_time(self):
        return self._wait_time

    ##Method that sets the wait time between letter in automatic mode
    #@param time Time between letter execution (Seconds)
    #
    def set_wait_time(self, time):
        self._wait_time = time

    ##Method that returns an array of all currently handled characters
    #
    def get_available_chars(self):
        return self._available_chars

    ##Method that toggles the current mode between automatic and semi-automatic
    #
    def toggle_semi_auto(self):
        self._semi_auto = not self._semi_auto
        EventHandler.Instance.trigger = not self._semi_auto
        Logger.Log("Semi auto: " + str(self._semi_auto) + "\n", 1)

    ##Method that returns a Boolean wether the configuration is currently semi-auto or not
    #
    def is_semi_auto(self):
        return self._semi_auto

    ##Method to set the purpose of the application
    #@param purpose New purpose to set
    #
    def set_purpose(self, purpose):
        self._purpose = purpose

    ##Method that returns the current purpose
    #
    def get_purpose(self):
        return self._purpose

    ##Method that returns the current purpose in String form
    #
    def get_purpose_string(self):
        if self.get_purpose() == Purpose.Purpose.Education:
            return "educ"
        elif self.get_purpose() == Purpose.Purpose.Quiz:
            return "quiz"


Instance = Configuration()
