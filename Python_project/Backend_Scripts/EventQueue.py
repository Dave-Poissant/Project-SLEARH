import threading
from Backend_Scripts import Event
from Backend_Scripts import Logger

class EventQueue:

    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    ##Method to prints the current length and state of the EventQueue
    #
    def __str__(self):
        _str = ""
        with self._lock:
            for _event in self._queue:
                _str = _str + " " + str(_event.get_name()) + " -"
            if _str == "":
                _str = "Empty "
            return "(" + str(len(self._queue)) + ") " + "Current queue state: " + _str[:-1]

    ##Method that clears all Events from the EventQueue
    #
    def clear_queue(self):
        with self._lock:
            self._queue.clear()

    ##Method that returns a Boolean to check if the EventQueue is currently empty or not
    #
    def is_empty(self):
        with self._lock:
            return len(self._queue) == 0

    ##Method that returns the current length of the EventQueue
    #
    def get_length(self):
        with self._lock:
            return len(self._queue)

    ##Method that removes the first element of the queue if it's not already empty
    #
    def dequeue(self):
        with self._lock:
            if not len(self._queue) == 0:
                Logger.Log("Dequeue '" + self._queue[0].get_name() + "'...\n", 3)
                self._queue.pop(0)
        Logger.Log(str(self) + "\n", 1)

    ##Method that return the next event in the queue (First event)
    #
    def first(self):
        with self._lock:
            if not len(self._queue) == 0:
                return self._queue[0]
        return None

    ## Method that return the last event in the queue
    #
    def last(self):
        with self._lock:
            if not len(self._queue) == 0:
                return self._queue[-1]
        return None

    ##Method to add an event to the EventQueue
    #@param event Event to add to the EventQueue
    #
    def add(self, event):
        with self._lock:
            #If event is 'High priority' it will be added at the beggining of the queue
            if event.is_high_priority(): 
                Logger.Log("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") high priority\n", 2)
                self._queue.insert(0, event)
            #If event is not 'High priority' it will be added at the end of the queue
            else:
                Logger.Log("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") low priority\n", 2)
                self._queue.append(event)
