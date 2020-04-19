import time
from Backend_Scripts import Configuration
import threading
from Backend_Scripts import Logger
from Backend_Scripts import EventQueue
from Backend_Scripts import EventType
from Backend_Scripts import Communication
from Backend_Scripts import Purpose
from Backend_Scripts import Quiz


class EventHandler:

    def __init__(self):
        self.should_run = True
        self._queue = EventQueue.EventQueue()
        self._thread = threading.Thread(target=self.private_thread)
        self.trigger = True
        self.__start_thread__()
        self.trigger_warned = False
        self.ui_adress = None

    ##Method that store the location of the UI in a pointer
    #@params adress Actual adress of the UI
    #
    def set_ui_adress(self, adress):
        self.ui_adress = adress

    ##Method that starts the EventHandler private thread
    #
    def __start_thread__(self):
        self._thread.start()

    ##Method that print the current state of the EventQueue
    #
    def __str__(self):
        return str(self._queue)

    ##Method that clears all the event from the EventQueue
    #
    def clear_queue(self):
        self._queue.clear_queue()

    ##Method that log the current state of the EventQueue
    #
    def print_queue(self):
        Logger.Log(self, 1)
        print("\n")

    ##Method that set the trigger to True to execute the next event in queue while in semi-auto mode
    #
    def next_letter(self):
        self.trigger = True
        self.trigger_warned = False
        Logger.Log('Trigger sent ...\n', 2)

    ##Method that returns a Boolean to check is the EventQueue is empty of not
    #
    def is_empty(self):
        return self._queue.is_empty()

    ##Method that return the EventQueue
    #
    def get_queue(self):
        return self._queue

    ##Method to add an event to the EventQueue
    #@params _event Event to be added to the queue
    #
    def add_event(self, _event):
        self._queue.add(_event)

    ##Method that handles the logic to execute an event according to the event_type and current configuration
    #@param event Event to be executed
    #
    def execute_event(self, event):

        if Configuration.Instance.get_purpose() == Purpose.Purpose.Quiz:  # Quiz Purpose

            if Quiz.Instance.get_current_letter() is None:
                Quiz.Instance.get_new_letter()

                Communication.Instance.update_stream(ord(Quiz.Instance.get_current_letter()),
                                                     Configuration.Instance.get_purpose_string(),
                                                     Configuration.Instance.get_wait_time())
                Communication.Instance.send_stream()
                self.ui_adress.change_state_picture(True, Quiz.Instance.get_current_letter())
                self.ui_adress.change_hand_ready_state(False)

                self.wait_arduino_ready_state()

                self.ui_adress.enable_entry()
                self.ui_adress.change_hand_ready_state(True)

            if event is None:
                return

            if not event.is_type(EventType.EventType.quiz_answer):
                Logger.Log("'" + str(event.get_type()) + "' is not a valid event type\n", 1)
            else:
                if Quiz.Instance.validate_answer(event.get_name()):  # Send new letter to hand if is valid answer
                    Communication.Instance.update_stream(ord(Quiz.Instance.get_current_letter()),
                                                         Configuration.Instance.get_purpose_string(),
                                                         Configuration.Instance.get_wait_time())
                    Communication.Instance.send_stream()
                    self.ui_adress.change_state_picture(True, Quiz.Instance.get_current_letter())
                    self.ui_adress.change_hand_ready_state(False)

                    self.wait_arduino_ready_state()

                    self.ui_adress.enable_entry()
                    self.ui_adress.change_hand_ready_state(True)
                    self.ui_adress.quiz_answer_conclusion(True)
                    self.ui_adress.modify_quiz_score()
                else:
                    self.ui_adress.enable_entry()
                    self.ui_adress.change_hand_ready_state(True)
                    self.ui_adress.quiz_answer_conclusion(False)

            self._queue.dequeue()

        elif Configuration.Instance.get_purpose() == Purpose.Purpose.Education:  # Education Purpose

            if event is None:
                return

            if event.is_type(EventType.EventType.invalid_letter):  # Invalid letter event
                Logger.Log("'" + event.get_name() + "' is not a valid character\n", 1)

                self._queue.dequeue()
                if self._queue.is_empty():
                    self.ui_adress.enable_entry()
                    self.ui_adress.change_hand_ready_state(True)
                    self.ui_adress.enable_radiobuttons()
                    self.ui_adress.change_state_picture(False, '')

            elif event.is_type(EventType.EventType.letter):  # Letter event

                # Only execute if in auto mode or if trigger is true
                if self.trigger:
                    Logger.Log("Executing letter '" + event.get_name() + "'...\n", 2)

                    Communication.Instance.update_stream(ord(event.get_name()),
                                                         Configuration.Instance.get_purpose_string(),
                                                         Configuration.Instance.get_wait_time())
                    Communication.Instance.send_stream()
                    self.ui_adress.change_state_picture(True, event.get_name())
                    self.ui_adress.change_hand_ready_state(False)

                    self.wait_arduino_ready_state()

                    self._queue.dequeue()

                    if Configuration.Instance.is_semi_auto():  # Reset the trigger if in semi automatic mode
                        self.ui_adress.change_hand_ready_state(True)
                        self.trigger = False
                    else:
                        time.sleep(int(Configuration.Instance.get_wait_time()))  # Delay between letters in automatic mode

                elif not self.trigger_warned:
                    if not self._queue.is_empty():
                        Logger.Log("Waiting for trigger...\n", 1)
                    else:
                        Logger.Log("Queue Empty...\n", 1)
                    self.trigger_warned = True

                if self._queue.is_empty():
                    self.ui_adress.enable_entry()
                    self.ui_adress.change_hand_ready_state(True)
                    self.ui_adress.enable_radiobuttons()
                    self.ui_adress.change_state_picture(False, '')

            else:
                Logger.Log("Event type is invalid\n", 2)

    ##Method that waits for the Arduino to send a ready state to the communication stream
    #
    def wait_arduino_ready_state(self):
        ready = False
        while not ready:
            string_state = Communication.Instance.read_stream()
            if string_state == "true":
                ready = True
            elif string_state == "false":
                ready = False
            elif string_state == "none":
                self._queue.clear_queue()
                self.ui_adress.no_connection_window()
                self.ui_adress.enable_entry()
                self.ui_adress.change_hand_ready_state(True)
                self.ui_adress.change_state_picture(False, '')
                break
            time.sleep(0.1)

    #Method that runs the EventHandler's private thread as long as should_run is True
    #
    def private_thread(self):
        while self.should_run:
            if not self._queue.is_empty():
                self.execute_event(self._queue.first())

    #Method that ends EventHandler's private thread
    #
    def end_thread(self):
        self.should_run = False
        self._thread.join()
        print("Event thread joined")


Instance = EventHandler()
