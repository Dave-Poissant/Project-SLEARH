import threading
import Event

class EventQueue:

    def __init__(self):
        self._queue = []
        self._lock = threading.Lock()

    def __str__(self):
        _str = ""
        for _event in self._queue:
            _str = _str + str(_event.get_name()) + " - "
        return "Current queue state: " + _str

    def is_empty(self):
        with self._lock:
            return len(self._queue) == 0


    #Removes the first element of the queue if it's not empty
    def dequeue(self):
        print("Dequeue '" + self._queue[0].get_name() + "'...")
        if not self.is_empty():
            with self._lock:
                self._queue.pop(0)
                print("(" + str(len(self._queue)) + ") " + str(self))
        else:
            print("already empty")

    #Return the next event in the queue
    def first(self):
        if not self.is_empty():
            with self._lock:
                return self._queue[0]
        return None

    def add(self, event):
        with self._lock:
            #If event is 'High priority' it will be added at the beggining of the queue
            if event.is_high_priority(): 
                print("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") high priority" )
                self._queue.insert(0, event)
            else:
                print("Event added: " + str(event.get_type()) + " (" + event.get_name() + ") low priority" )
                self._queue.append(event)
