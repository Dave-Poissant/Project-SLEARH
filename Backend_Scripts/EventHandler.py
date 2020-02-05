
from EventQueue import EventQueue
from EventType import EventType
import Configuration
import logging
import threading

class EventHandler:

    def __init__(self):
        self._queue = EventQueue()
        self._thread = threading.Thread(target=self.private_thread)
        self.trigger = True
        
    def __start_thread__(self):
        self._thread.start()

    def add_event(self, _event):
        self._queue.add(_event)

    def execute_event(self, event):
        logging.log(1, "Executing event of type " + str(event.get_type()))

        if event.is_type(EventType.next_letter):

            self.trigger = True

        elif event.is_type(EventType.invalid_letter):

            logging.warning(event.get_name() + " is not a valid character")

            #TODO : handle events of type 'invalid_letter'

            self._queue.dequeue()

        elif event.is_type(EventType.letter):
            if not Configuration.Instance.is_semi_auto() | self.trigger:

                logging.log(1, "Executing letter '" + event.get_name() + "'")

                #TODO : handle events of type 'letter'

                self._queue.dequeue()
        else:
            logging.error("Event type is invalid")


    def private_thread(self):
        while True:
            if not self._queue.is_empty():
                self.execute_event(self._queue.first())




Instance = EventHandler()