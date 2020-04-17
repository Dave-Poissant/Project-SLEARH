import random
from Backend_Scripts import Configuration
from Backend_Scripts import Logger

class Quiz:
    def __init__(self):
        self._current_letter = None
        self._last_letter = None
        self._score = 0
        self.ui_adress = None

    def set_ui_adress(self, adress):
        self.ui_adress = adress

    def reset(self):
        self._current_letter = None
        self._last_letter = None
        self.reset_score()

    def reset_score(self):
        self._score = 0
        self.ui_adress.modify_quiz_score()

    def get_score(self):
        return self._score

    def increment_score(self):
        self._score += 1

    def get_current_letter(self):
        return str(self._current_letter)

    def get_new_letter(self):
        self._last_letter = self._current_letter
        self._current_letter = self._random_letter()

    def _random_letter(self):
        is_same_as_last = True
        rnd_letter = None

        while is_same_as_last:
            rnd_int = random.randint(0, len(Configuration.Instance._available_chars) - 1)
            rnd_letter = Configuration.Instance._available_chars[rnd_int]
            if not rnd_letter == self._last_letter:
                is_same_as_last = False

        Logger.Log("New random letter: " + str(rnd_letter), 1)
        return rnd_letter

    def validate_answer(self, answer):
        is_valid = (str(answer).lower() == self.get_current_letter().lower())
        if is_valid:
            self.increment_score()
            self.get_new_letter()
            Logger.Log("Good Answer! (" + str(answer) + ")", 1, Logger.Color.BLUE)
        else:
            Logger.Log("Wrong Answer! :( (" + str(answer) + ")",  1, Logger.Color.RED)
        return is_valid


Instance = Quiz()

