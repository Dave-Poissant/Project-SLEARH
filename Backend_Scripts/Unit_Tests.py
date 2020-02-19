import Configuration
import TextAnalyser
import EventHandler
import time
from EventType import EventType
import Logger
import os

config = Configuration.Instance
textAnalyser = TextAnalyser.TextAnalyser()
e_Handler = EventHandler.Instance


def get_valid_string():
    available_chars = config.get_available_chars()
    _str = ""
    for _char in available_chars:
        _str = _str + _char
    Logger.Log("valid string: " + _str, 0)
    return _str

valid_string = get_valid_string()

def run():
    config.set_debug(True, 0)
    failed = 0
    passed = 0

    Logger.Log("Unit tests:", 0, Logger.Color.UNDERLINE)

    active_tests = [queue_dequeue,  queue_status, valid_char, invalid_char, semi_auto, auto, wait_time]

    for func in active_tests:
        if func():
            passed = passed + 1
        else:
            failed = failed + 1

        e_Handler.get_queue().clear_queue()
    
    Logger.Log("All done! " + "(" + str(passed) + " Passed) (" + str(failed) + " Failed)", 0, Logger.Color.BOLD)

def print_result(test, result):
    if result:
        Logger.Log(test + " test: " + Logger.Color.GREEN.value + "Passed" + Logger.Color.ENDC.value, 0)
    else:
        Logger.Log(test + " test: " + Logger.Color.RED.value + "Failed" + Logger.Color.ENDC.value, 0)
    return result

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


def valid_char():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char(valid_string)

    while not e_Handler.get_queue().is_empty() and sucess:
        sucess = sucess and e_Handler.get_queue().first().is_type(EventType.letter)
        e_Handler.get_queue().dequeue()
    
    return print_result("Valid characters", sucess)

def invalid_char():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    textAnalyser.parse_char("*/#)(")

    while e_Handler.get_queue().get_length() > 0 and sucess:
        sucess = sucess and e_Handler.get_queue().first().is_type(EventType.invalid_letter)
        e_Handler.get_queue().dequeue()

    return print_result("Invalid characters", sucess)

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

def queue_status():
    e_Handler.clear_queue()
    sucess = True

    if not config.is_semi_auto():
        config.toggle_semi_auto()
        
    sucess = e_Handler.get_queue().get_length() == 0
        
    textAnalyser.parse_char(valid_string[0])

    sucess = sucess and e_Handler.get_queue().get_length() == 1

    return print_result("Queue Status", sucess)

def wait_time():
    e_Handler.clear_queue()
    sucess = True

    test_wait_time = 3

    if not config.is_semi_auto():
        config.toggle_semi_auto()

    config.set_wait_time(test_wait_time)
    sucess = sucess and config.get_wait_time() == test_wait_time

    #Logger.Log(str(sucess) + ' wait time: ' + str(config.get_wait_time()), 0)
    textAnalyser.parse_char(valid_string[0] + valid_string[0])

    original_length = e_Handler.get_queue().get_length()
    config.toggle_semi_auto()


    for _ in range(0, test_wait_time):
        sucess = sucess and e_Handler.get_queue().get_length() == original_length
        #Logger.Log('Success: ' + str(sucess) + ' - waited : ' + str(i) + 's expected length: '  + str(original_length) + ' and got length: ' + str(e_Handler.get_queue().get_length()), 0)
        time.sleep(1)

    time.sleep(1)
    sucess = sucess and e_Handler.get_queue().get_length() == original_length - 1
    #Logger.Log('Success: ' + str(sucess) + ' - waited : ' + str(test_wait_time) + 's expected length: '  + str(original_length - 1) + ' and got length: ' + str(e_Handler.get_queue().get_length()), 0)

    return print_result('Wait time', sucess)















    

