from Backend_Scripts import Configuration
import os
from enum import Enum

##Enum that contains all color option for the Logger
#
class Color(Enum):
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

##Method that logs a string at a given debug level
#@param _str String to be logged
#@param _lvl Int Debug level of this log
#@param _color Color of the logger string
#
def Log(_str, _lvl = 1, _color = None):
    os.system('color')
    if Configuration.Instance.get_debug_state and _lvl <= Configuration.Instance.get_debug_level():
        if _color == None:
            print(_str)
        else:
            print(_color.value + _str + Color.ENDC.value)
