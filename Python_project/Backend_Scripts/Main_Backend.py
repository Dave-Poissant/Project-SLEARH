from Backend_Scripts import TextAnalyser
from Backend_Scripts import EventHandler
from Backend_Scripts import Configuration
import time
from Backend_Scripts import Unit_Tests
from Backend_Scripts import Event
from Backend_Scripts import EventType

##Debug Purposes
#
    
def func():
    config = Configuration.Instance
    e_handler = EventHandler.Instance
    analyser = TextAnalyser.TextAnalyser()

    config.set_debug(True, 1)
    config.set_wait_time(0)
    config.toggle_semi_auto()

    analyser.parse_char("aa3Aat ")
    analyser.parse_char("bbbb ")
    e_handler.print_queue()

    while not e_handler.is_empty():
        time.sleep(3)
        e_handler.next_letter()

    analyser.parse_char("bbbb ")
    e_handler.print_queue()
    config.toggle_semi_auto()

def main():
    #Unit_Tests.run()
    func()

if __name__ == "__main__":
    main()