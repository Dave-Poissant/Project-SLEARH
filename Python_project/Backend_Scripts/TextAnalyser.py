from Backend_Scripts import Configuration
from Backend_Scripts import EventHandler
from Backend_Scripts import Logger
from Backend_Scripts import Event
from Backend_Scripts import EventType

class TextAnalyser:

    def __init__(self):
        pass
    # Add an event to the event queue
    def push_event(self, _event):
        EventHandler.Instance.add_event(_event) 

    # Check each letter of a string and create related events
    def parse_char(self, _str):
        _str = _str.lower()
        for char in _str:
            if not char.isspace(): #skip char if it's a whitespace
                if self.is_char_valid(char) or self.is_char_valid(char.upper()):
                    Logger.Log("char parsed: " + char + " (valid)\n", 3)
                    self.push_event(Event.Event(char, EventType.EventType.letter))
                else:
                    Logger.Log("char parsed: " + char + " (invalid)\n", 3)
                    self.push_event(Event.Event(char, EventType.EventType.invalid_letter, True))

    # Check if a char is available
    def is_char_valid(self, char):
        return char in Configuration.Instance.get_available_chars()

instance = TextAnalyser()