
import TextAnalyser
import EventHandler
import Configuration
from Event import Event
from EventType import EventType
import time

def main():

    config = Configuration.Instance
    ev = EventHandler.Instance
    analyser = TextAnalyser.TextAnalyser()

    config.set_wait_time(2)
    #config.toggle_semi_auto()
    
    analyser.parse_char("a3Aat ")
    analyser.parse_char("bbbb ")

    while not ev.is_empty():
        ev.get_queue()
        print("\n")
        time.sleep(5)
        ev.add_event(Event("next", EventType.next_letter, True ))
    


main()