import threading
import Event
import Logger

class EventQueue:

    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    def __str__(self):
        _str = ""
        with self._lock:
            for _event in self._queue:
                _str = _str + " " + str(_event.get_name()) + " -"
            if _str == "":
                _str = "Empty "
            return "(" + str(len(self._queue)) + ") " + "Current queue state: " + _str[:-1]

    def clear_queue(self):
        with self._lock:
            self._queue.clear()

    def is_empty(self):
        with self._lock:
            return len(self._queue) == 0

    def get_length(self):
        with self._lock:
            return len(self._queue)

    #Removes the first element of the queue if it's not empty
    def dequeue(self):
        with self._lock:
            if not len(self._queue) == 0:
                Logger.Log("Dequeue '" + self._queue[0].get_name() + "'...\n", 3)
                self._queue.pop(0)
        Logger.Log(str(self) + "\n", 1)

    #Return the next event in the queue
    def first(self):
        with self._lock:
            if not len(self._queue) == 0:
                return self._queue[0]
        return None

    #Return the next event in the queue
    def last(self):
        with self._lock:
            if not len(self._queue) == 0:
                return self._queue[-1]
        return None

    def add(self, event):
        with self._lock:
            #If event is 'High priority' it will be added at the beggining of the queue
            if event.is_high_priority(): 
                Logger.Log("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") high priority\n", 2)
                self._queue.insert(0, event)
            else:
                Logger.Log("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") low priority\n", 2)
                self._queue.append(event)
