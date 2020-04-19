from Backend_Scripts import Configuration
from Backend_Scripts import TextAnalyser
from Backend_Scripts import EventHandler
import time
from Backend_Scripts import Logger
import os
from Backend_Scripts import Event
from Backend_Scripts import EventType


config = Configuration.Instance
textAnalyser = TextAnalyser.TextAnalyser()
e_Handler = EventHandler.Instance

##Method that return a string of valid characters
#
def get_valid_string():
    available_chars = config.get_available_chars()
    _str = ""
    for _char in available_chars:
        _str = _str + _char
    Logger.Log("valid string: " + _str, 0)
    return _str

valid_string = get_valid_string()

##Method that runs all unit tests and logs their results
#
def run():
    config.set_debug(True, 0)
    failed = 0
    passed = 0

    Logger.Log(Logger.Color.BOLD.value + "Unit tests:" + Logger.Color.ENDC.value, 0, Logger.Color.UNDERLINE)

    active_tests = [queue_dequeue,  queue_status, valid_char, invalid_char, semi_auto, auto, wait_time, high_priority]

    for func in active_tests:
        if func():
            passed = passed + 1
        else:
            failed = failed + 1

        e_Handler.get_queue().clear_queue()
    
    Logger.Log("All done! " + "(" + str(passed) + " Passed) (" + str(failed) + " Failed)", 0, Logger.Color.BOLD)

##Method that print the result for a test
#@param test String, Name of the unit test to print
#@param result Boolean Result of the unit test
#
def print_result(test, result):
    if result:
        Logger.Log(test + " test: " + Logger.Color.GREEN.value + "Passed" + Logger.Color.ENDC.value, 0)
    else:
        Logger.Log(test + " test: " + Logger.Color.RED.value + "Failed" + Logger.Color.ENDC.value, 0)
    return result

##Unit test to validate the dequeue method
#
def queue_dequeue():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char(valid_string[0])

    sucess = e_Handler.get_queue().get_length() == 1

    e_Handler.get_queue().dequeue()

    sucess =  sucess and e_Handler.get_queue().is_empty() 

    return print_result('Add/Dequeue Queue', sucess)

##Unit test to validate that all valid char works as intended
#
def valid_char():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char(valid_string)

    while not e_Handler.get_queue().is_empty() and sucess:
        sucess = sucess and e_Handler.get_queue().first().is_type(EventType.EventType.letter)
        e_Handler.get_queue().dequeue()
    
    return print_result("Valid characters", sucess)

##Unit to test to validate that invalid chars are handled as intended
#
def invalid_char():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char("*/#)(")

    while e_Handler.get_queue().get_length() > 0 and sucess:
        sucess = sucess and e_Handler.get_queue().first().is_type(EventType.EventType.invalid_letter)
        e_Handler.get_queue().dequeue()

    return print_result("Invalid characters", sucess)

##Unit test to validate that the semi_auto mode works as intended
#
def semi_auto():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    sucess = not e_Handler.trigger
    textAnalyser.parse_char(valid_string)
    
    queue_length = e_Handler.get_queue().get_length()

    e_Handler.next_letter()

    i = 0
    while e_Handler.get_queue().get_length() == queue_length and i < 10: #wait for dequeue
        time.sleep(0.5)
        i = i + 1

    sucess = e_Handler.get_queue().get_length() == queue_length  - 1 and not e_Handler.trigger and sucess
   
    return print_result("Semi-auto", sucess)

##Unit test to validate that the automatic mode works as intended
#
def auto():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char(valid_string)

    queue_length = e_Handler.get_queue().get_length()

    config.toggle_semi_auto()
    sucess = e_Handler.trigger and sucess

    i = 0
    while e_Handler.get_queue().get_length() == queue_length and i < 10: #wait for dequeue
        time.sleep(0.5)
        i = i + 1

    sucess = e_Handler.get_queue().get_length() < queue_length and e_Handler.trigger and sucess
   
    return print_result("Auto", sucess)

##Unit test that validates that the queue status is as intended
#
def queue_status():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()
        
    sucess = e_Handler.get_queue().get_length() == 0
        
    textAnalyser.parse_char(valid_string[0])

    sucess = sucess and e_Handler.get_queue().get_length() == 1

    return print_result("Queue Status", sucess)

##Unit test that validates that the wait_time feature in auto mode works as intended
#
def wait_time():
    e_Handler.clear_queue()
    sucess = True

    test_wait_time = 3

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    config.set_wait_time(test_wait_time)
    sucess = sucess and config.get_wait_time() == test_wait_time

    Logger.Log(str(sucess) + ' wait time: ' + str(config.get_wait_time()), 0.5)
    textAnalyser.parse_char(valid_string[0] + valid_string[0])

    original_length = e_Handler.get_queue().get_length()
    config.toggle_semi_auto()


    for i in range(0, test_wait_time):
        sucess = sucess and e_Handler.get_queue().get_length() == original_length
        Logger.Log('Success: ' + str(sucess) + ' - waited : ' + str(i) + 's expected length: '  + str(original_length) + ' and got length: ' + str(e_Handler.get_queue().get_length()), 0.5)
        time.sleep(1)

    time.sleep(1)
    sucess = sucess and e_Handler.get_queue().get_length() == original_length - 1
    Logger.Log('Success: ' + str(sucess) + ' - waited : ' + str(test_wait_time) + 's expected length: '  + str(original_length - 1) + ' and got length: ' + str(e_Handler.get_queue().get_length()), 0.5)

    return print_result('Wait time', sucess)


##Unit test that validate that the High_Priority feature works as intended
#
def high_priority():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char(valid_string)
    textAnalyser.push_event(Event.Event('first', EventType.EventType.letter, True))
    textAnalyser.push_event(Event.Event('last', EventType.EventType.letter, False))
    
    sucess = sucess and e_Handler.get_queue().first().get_name() == 'first' and e_Handler.get_queue().last().get_name() == 'last'

    Logger.Log('Excpected "first" got "' +  str(e_Handler.get_queue().first().get_name()), 0.5)
    Logger.Log('Excpected "last" got "' +  str(e_Handler.get_queue().last().get_name()), 0.5)

    return print_result("High priority", sucess)
    
















    

