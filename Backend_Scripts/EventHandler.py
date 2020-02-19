import time
from Backend_Scripts import Configuration
import threading
from Backend_Scripts import Logger
from Backend_Scripts import EventQueue
from Backend_Scripts import EventType

class EventHandler:

    def __init__(self):
        self._queue = EventQueue.EventQueue()
        self._thread = threading.Thread(target=self.private_thread)
        self.trigger = True
        self.__start_thread__()
        self.trigger_warned = False
        self.should_run = True
        
    def __start_thread__(self):
        self._thread.start()

    def __str__(self):
        return str(self._queue)

    def clear_queue(self):
        self._queue.clear_queue()

    def print_queue(self):
        Logger.Log(self, 1)
        print("\n")

    def next_letter(self):
        self.trigger = True
        self.trigger_warned = False
        Logger.Log('Trigger sent ...\n', 2)

    def is_empty(self):
        return self._queue.is_empty()

    def get_queue(self):
        return self._queue

    def add_event(self, _event):
        self._queue.add(_event)

    def execute_event(self, event):
        if event is None:
            return
            
        if event.is_type(EventType.EventType.invalid_letter): # Invalid letter event
            Logger.Log("'" + event.get_name() + "' is not a valid character\n", 1)

            #TODO : handle events of type 'invalid_letter'

            self._queue.dequeue()

        elif event.is_type(EventType.EventType.letter): # Letter event

            #Only execute if in auto mode or if trigger is true
            if self.trigger: 
                Logger.Log("Executing letter '" + event.get_name() + "'...\n", 2)

                #TODO : handle events of type 'letter'

                self._queue.dequeue()

                if Configuration.Instance.is_semi_auto(): # Reset the trigger if in semi automatic mode
                    self.trigger = False
                else:
                    time.sleep(int(Configuration.Instance.get_wait_time())) # Delay between letters in automatic mode

            elif not self.trigger_warned:
                if not self._queue.is_empty():
                    Logger.Log("Waiting for trigger...\n", 1)
                else:
                    Logger.Log("Queue Empty...\n", 1)
                self.trigger_warned = True


        else:
            Logger.Log("Event type is invalid\n", 2)

    def private_thread(self):
        while self.should_run:
            if not self._queue.is_empty():
                self.execute_event(self._queue.first())

    def end_thread(self):
        self.should_run = False
        self._thread.join()


Instance = EventHandler()

