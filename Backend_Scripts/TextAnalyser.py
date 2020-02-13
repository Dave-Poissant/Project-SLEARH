
import Configuration
import EventHandler
from Event import Event
from EventType import EventType

class TextAnalyser:

    def __init__(self):
        pass

    # Check each letter of a string and create related events
    def parse_char(self, _str):
        _str = _str.lower()
        for char in _str:
            if not char.isspace(): #skip if whitespace
                if self.is_char_valid(char):
                    print("char parsed: " + char + " (valid)\n")
                    self.push_event(Event(char, EventType.letter))
                else:
                    print("char parsed: " + char + " (invalid)\n")
                    self.push_event(Event(char, EventType.invalid_letter))

    # Check if a char is available
    def is_char_valid(self, char):
        return char in Configuration.Instance.get_available_chars()

    # Add an event to the event queue
    def push_event(self, _event):
        EventHandler.Instance.add_event(_event) 