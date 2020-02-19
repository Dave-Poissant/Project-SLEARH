import Configuration
import os
from enum import Enum

class Color(Enum):
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Log(_str, _lvl = 1, _color = None):
    os.system('color')
    if Configuration.Instance.debug and _lvl <= Configuration.Instance.debug_level:
        if _color == None:
            print(_str)
        else:
            print(_color.value + _str + Color.ENDC.value)
