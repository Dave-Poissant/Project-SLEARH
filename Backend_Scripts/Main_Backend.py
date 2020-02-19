import TextAnalyser
import EventHandler
import Configuration
import time
import Unit_Tests
from Event import Event
from EventType import EventType

    
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
    Unit_Tests.run()
    #func()


main()