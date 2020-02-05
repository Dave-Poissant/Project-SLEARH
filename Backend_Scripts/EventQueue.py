import threading
import Event

class EventQueue:

    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    def is_empty(self):
        with self._lock:
            return len(self._queue) > 0

    #Removes the first element of the queue if it's not empty
    def dequeue(self):
        if not self.is_empty:
            with self._lock:
                self._queue.pop(0)

    #Return the next event in the queue
    def first(self):
        if not self.is_empty():
            with self._lock:
                return self._queue[0]
        return None

    def add(self, event):
        if isinstance(event, Event):
            with self._lock:
                if event.is_high_priority: #If event is 'High priority' it will be added at the beggining of the queue
                    self._queue.insert(0, event)
                else:
                    self._queue.append(event)