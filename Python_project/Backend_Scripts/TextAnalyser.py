from Backend_Scripts import Configuration
from Backend_Scripts import EventHandler
from Backend_Scripts import Logger
from Backend_Scripts import Event
from Backend_Scripts import EventType
from Backend_Scripts import Purpose

class TextAnalyser:

    def __init__(self):
        self.ui_adress = None

    def set_ui_adress(self, adress):
        self.ui_adress = adress

    # Add an event to the event queue
    def push_event(self, _event):
        EventHandler.Instance.add_event(_event) 

    # Check each letter of a string and create related events
    def parse_char(self, _str):
        _str = _str.lower()

        if Configuration.Instance.get_purpose() == Purpose.Purpose.Education:
            not_handled_chars = ""
            for char in _str:
                if not char.isspace():  # skip char if it's a whitespace
                    if self.is_char_valid(char) or self.is_char_valid(char.upper()):
                        Logger.Log("char parsed: " + char + " (valid)\n", 3)
                        self.push_event(Event.Event(char, EventType.EventType.letter))
                    else:
                        Logger.Log("char parsed: " + char + " (invalid)\n", 3)
                        not_handled_chars = not_handled_chars + char
                        self.push_event(Event.Event(char, EventType.EventType.invalid_letter, True))
            if not_handled_chars != "":
                self.ui_adress.not_handled_chars_window(not_handled_chars)

        elif Configuration.Instance.get_purpose() == Purpose.Purpose.Quiz:
            if len(_str) > 1:
                Logger.Log("Too many character! Please enter a single letter for Quiz mode")
                return False
            else:
                Logger.Log("Quiz answer pushed (" + _str + ")", 2)
                self.push_event(Event.Event(_str, EventType.EventType.quiz_answer))

        return True

    # Check if a char is available
    def is_char_valid(self, char):
        return char in Configuration.Instance.get_available_chars()

instance = TextAnalyser()