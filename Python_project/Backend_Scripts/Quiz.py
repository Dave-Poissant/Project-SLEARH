import random
from Backend_Scripts import Configuration
from Backend_Scripts import Logger

class Quiz:
    def __init__(self):
        self._current_letter = None
        self._last_letter = None
        self._score = 0
        self.ui_adress = None

    ##Method that store the adress of the UI in a pointer
    #@param adress Actual adress of the UI
    #
    def set_ui_adress(self, adress):
        self.ui_adress = adress

    ##Method that resets the quiz progression
    #
    def reset(self):
        self._current_letter = None
        self._last_letter = None
        self.reset_score()

    ##Method that resets the quiz score
    #
    def reset_score(self):
        self._score = 0
        self.ui_adress.modify_quiz_score()

    ##Method that returns the current Quiz score
    #
    def get_score(self):
        return self._score

    ##Method that increment the Quiz score by 1
    #
    def increment_score(self):
        self._score += 1

    ##Method that returns the current letter to guess
    #
    def get_current_letter(self):
        return str(self._current_letter)

    ##Method that sets a new random letter and store the last guessed letter
    #
    def get_new_letter(self):
        self._last_letter = self._current_letter
        self._current_letter = self._random_letter()

    ##Method that returns a random letter from the Configuration.available_chars array
    #
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

    ##Method that checks and returns if a given answer is valid and handles it accordingly.
    #@param answer char User answer to be validated
    #
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

