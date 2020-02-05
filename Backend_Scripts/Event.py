
import EventType

class Event:

    def __init__(self, name, event_type, priority = False):
        self._name = name
        self._type = event_type
        self._high_priority = priority

    def is_high_priority(self):
        return self._high_priority

    def get_type(self):
        return self._type
        
    def get_name(self):
        return self._name

    def is_type(self, _type):
        return self._type == _type