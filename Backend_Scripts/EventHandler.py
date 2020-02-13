
from EventQueue import EventQueue
from EventType import EventType
import time
import Configuration
import threading

class EventHandler:

    def __init__(self):
        self._queue = EventQueue()
        self._thread = threading.Thread(target=self.private_thread)
        self.trigger = True
        self.__start_thread__()
        self.warned = False
        
    def __start_thread__(self):
        self._thread.start()

    def is_empty(self):
        return self._queue.is_empty()

    def get_queue(self):
        print(self._queue)
        return self._queue

    def add_event(self, _event):
        self._queue.add(_event)

    def execute_event(self, event):
        if event.is_type(EventType.next_letter): # Next letter event
            self.trigger = True
            self.warned = False
            self._queue.dequeue()

        elif event.is_type(EventType.invalid_letter): # Invalid letter event
            print(event.get_name() + " is not a valid character")

            #TODO : handle events of type 'invalid_letter'

            self._queue.dequeue()

        elif event.is_type(EventType.letter): # Letter event

            #Only execute if in auto mode or if trigger is true
            if not Configuration.Instance.is_semi_auto() or self.trigger: 
                print("Executing letter '" + event.get_name() + "'...")

                #TODO : handle events of type 'letter'

                if Configuration.Instance.is_semi_auto(): # Reset the trigger if in semi automatic mode
                    self.trigger = False
                else:
                    time.sleep(Configuration.Instance.get_wait_time()) # Delay between letters in automatic mode

                self._queue.dequeue()

            elif not self.warned:
                print("Waiting for trigger...")
                self.warned = True

        else:
            print("Event type is invalid")


    def private_thread(self):
        while True:
            if not self._queue.is_empty():
                self.execute_event(self._queue.first())


Instance = EventHandler()

