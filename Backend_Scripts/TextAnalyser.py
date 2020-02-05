
import Configuration
import EventHandler
from Event import Event
from EventType import EventType

class TextAnalyser:

    def parse_char(self, str):
        for char in str:
            if self.is_char_valid(char):
                self.push_event(Event(char, EventType.letter))
            else:
                self.push_event(Event(char, EventType.invalid_letter))

    def is_char_valid(self, char):
        return char in Configuration.Instance.get_available_chars()

    def push_event(self, _event):
        EventHandler.Instance.add_event(_event) 