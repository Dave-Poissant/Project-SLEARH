
import EventType

class Event:

    def __init__(self, name, event_type, priority = False):
        self._name = name
        self._type = event_type
        self._high_priority = priority #High priority Events will be added at the start of the EventQueue

    def is_high_priority(self):
        return self._high_priority

    def get_type(self):
        return self._type
        
    def get_name(self):
        return self._name

    def is_type(self, a_type):
        #print(str(self._type) + " = " + str(a_type) + "? : " + str(self._type == a_type))
        return self._type == a_type