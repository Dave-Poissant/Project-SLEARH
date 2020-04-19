from Backend_Scripts import EventType

class Event:

    def __init__(self, name, event_type, priority = False):
        self._name = name
        self._type = event_type
        self._high_priority = priority #High priority Events will be added at the start of the EventQueue

    ##Method that return if the event is High priority
    #
    def is_high_priority(self):
        return self._high_priority

    ##Method that returns the event type of this event
    #
    def get_type(self):
        return self._type

    ##Method that returns the name of this event
    #
    def get_name(self):
        return self._name

    ##Method that returns a Boolean to check if this event is a given type
    #@params a_type Event_type enum value to check against
    #
    def is_type(self, a_type):
        return self._type == a_type