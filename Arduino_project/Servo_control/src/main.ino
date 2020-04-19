/** @file main.ino
 * @brief This file is the main program of the arduino project.
 * 
 * This file contains the main loop of the project.
 * @author CHARBONNEAU, EMILE
 * @date 19/04/2020
 */
#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <CommunicationArduino.h>
#include "SoftTimer/SoftTimer.h"
#include "Servo.h"
/**
 * @headerfile Arduino.h "Arduino.h"
 * @headerfile string.h "string.h"
 * @headerfile Wire.h "Wire.h"
 * @headerfile CommunicationArduino.h "ArduinoCommunication.h"
 * @headerfile SoftTime/SoftTime.h "SoftTime/SoftTime.h"
 * @headerfile Servo.h "Servo.h"
 */

/** The next defined are the different communication state.
 */
#define NOT_READY_TO_SEND     false                       ///< Init. to false.
#define READY_TO_SEND         true                        ///< Init. to true.
#define NOT_READY_TO_READ     false                       ///< Init. to false.
#define READY_TO_READ         true                        ///< Init. to true.

/** The next defined are the different communication delays.
 */
#define SEND_UPDATE_PERIODE   200                         ///< sent of Read state Periode (ms)
#define READ_UPDATE_PERIODE   1000                        ///< read of Serial Periode (ms)
#define BAUD                  9600                        ///< Baud rate for Arduino mega 2560
#define LOOP_DELAY            200                         ///< time delay between each finger mouvment
#define TIME_ON_LETTER        1000                        ///< Time spent on each letter. Init. to 1 sec.

/** @brief The next defined are the different purposes.
 * The different purposes are Education and Quiz.
 * The logic of the main loop alters corresponding to the selected purpose.
 */
#define EDUCATION             0
#define QUIZ                  1
#define UNFOUND               2

/** Function prototypes
 */
void sendTimerCallback();                                 ///< callback to update the send Serial.read state
void resetTimer();                                        ///< callback to reset time spend on letter

/** Other variables
 * Communication variables:
 */
CommunicationArduino comObject = CommunicationArduino();  ///< Only instance of CommunicationArduino class, to send and read from python UI
volatile bool shouldSend = NOT_READY_TO_SEND;             ///< flag to send a message
volatile bool shouldRead = NOT_READY_TO_READ;             ///< flag to read a message
bool messageReceived = false;                             ///< flag to show if the arduino as already received a message (temporary) 
SoftTimer timerSendMsg;                                   ///< send messages timer
SoftTimer timerReadMsg;                                   ///< read messages timer (temporary)
SoftTimer timerOnLetter;                                  ///< Monitors the time spent on each letter before resetting to initial position

/** Initiating the Servo class object.
 */
Servo servo;

/** command variables
 */
bool moveDone = false;                                    ///< Flag to control the main loop according to if the hand finished moving to the desired character
bool reverseDone = false;                                 ///< Flag to control the main loop according to if the hand finished moving back to it's initial position
bool newCommand = false;                                  ///< Normaly initialized to 0. Set to 1 for testing purposes.
bool blinkState = false;                                  ///< built-in LED's blinkState
int increment = 0;                                        ///< Increment to control which finger is it's turn to be moved
int decrement = NB_FINGERS-1;                             ///< Decrement to control which finger is it's turn to be moved back to initial position
int lastCommand = toAscii(' ');                           ///< Memorizing the last command achieved in this variable
int command = ' ';                                        ///< Memorizing the character to be displayed by the hand
int purpose = UNFOUND;                                    ///< Memorizing in which mode the application is used (Quiz or educationnal)
int timeOnLetter = 1;                                     ///< Memorizing the time that has to be spent on each letter
bool timerDone = false;                                   ///< Flag for the timer of the time spent on each letter


/** Setup
 */
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD);
  /** Initializing the timer to send the state to the Pi
   */
  timerSendMsg.setDelay(SEND_UPDATE_PERIODE);
  timerSendMsg.setCallback(sendTimerCallback);
  timerSendMsg.enable();
  /** Initializing the timer to handle the time spent on each letter
   */
  timerOnLetter.setDelay(TIME_ON_LETTER);
  timerOnLetter.setCallback(resetTimer);
  timerOnLetter.enable();
  /** initializing the pwm
   */
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);                              ///< Analog servos run at ~60Hz updates. 
  /** Placing every fingers to the initial position
   */
  for(int increment = 0; increment<NB_FINGERS; increment++){
    servo.servoOut('5',increment);
  }
}
/** @fn void setup()
 * @brief This function is the setup of the program.
 * @return This function doesn't return (void).
 */

void loop() {
  /** This section is executed if the arduino should send state to Pi.
   */
  if(shouldSend)
  {
    comObject.sendState(shouldRead);                      ///< Sends the state to the Pi.
  }
  /** This section is executed if the Arduino's state is not ready.
   */
  if(shouldRead == NOT_READY_TO_READ){
    /** This section is executed if the purpose is Education.
     */
    if(purpose != QUIZ){
      /** This section is executed if the hand hasn't finished it's moved
       * and the return value of servoOut() is true.
       */
      if(!moveDone && servo.servoOut(command,increment)){
        moveDone = true;                                  ///< If the code enters this section, the move is done.
      }
      /** This section is executed if the time on letter timer has elapsed.
       */
      if(timerDone){
        /** This section is executed if the move is done and
         * the return value of reverseMove() is true.
         */
        if(moveDone && servo.reverseMove(command, decrement)){
          reverseDone = true;                             ///< If the code enters this section, the reverse move is done.
          shouldRead = READY_TO_READ;                     ///< The move is finished. The arduino's state is ready.
          increment = 0;                                  ///< Increment is reset to 0.
          decrement = NB_FINGERS-1;                       ///< Decrement is reset to nb of fingers - 1.
          lastCommand = command;                          ///< Saving the actual command in memory &lastCommand.
          command = ' ';                                  ///< Command is reset to ' '.
        }
      }
      /** The the next if defines wich one of the increment or decrement to operate
       * on, depending on the conditions of the hand.
       */
      if(!moveDone){increment++;}                               ///< Incrementing
      if(timerDone && moveDone && !reverseDone){decrement--;}   ///< Decrementing
    }
    /** This section is executed if the purpose is Quiz.
     */
    else if(purpose == QUIZ){
      /** This section is executed if the last command is a character.
       */
      if(lastCommand != toAscii(' ')){
        /** This section is executed if the reverse move hasn't been done
         * and if the return value of reverseMove() is true.
         */
        if(!reverseDone && servo.reverseMove(lastCommand, decrement)){
          reverseDone = true;                             ///< If the code enters this section, the reverse move is done.
        }
        /** This section is executed if the reverse move is done
         * and if the return value of servoOut() is true.
         */
        if(reverseDone && servo.servoOut(command, increment)){
          /** This section is executed if the time on letter timer has elapsed.
           */
          if(timerDone){
            moveDone = true;                              ///< If the code enters this section, the move is done.
            shouldRead = READY_TO_READ;                   ///< The move is done. The arduino's state is ready.
            increment = 0;                                ///< Increment is reset to 0.
            decrement = NB_FINGERS-1;                     ///< Decrement is reset to nb of fingers - 1.
            lastCommand = command;                        ///< Saving the actual command in memory &lastCommand.
            command = ' ';                                ///< Command is reset to ' '.
          }
        }
      }
      /** The next if defines wich one of the increment or decrement to operate
       * on, depending on the conditions of the hand.
       */
      if(!reverseDone){decrement--;}                            ///< Incrementing
      if(timerDone && reverseDone && !moveDone){increment++;}   ///< Decrementing
    }
  }
  /** End of the not ready to read case
   */

  /** This section is executed if the arduino's state is ready to read.
   */
  if(shouldRead == READY_TO_READ){
    moveDone = false;                                           ///< Resetting moveDone to false.
    reverseDone = false;                                        ///< Resetting reverseDone to false.
    comObject.readCommand(&command, &purpose, &timeOnLetter);   ///< Reading informations about incoming command.
    /** This section is executed if the command is not empty.
     */
    if(command != toAscii(' ')){                               
      shouldRead = NOT_READY_TO_READ;                           ///< The state of the arduino is set to not ready because it received a valid command.
      timerOnLetter.setDelay(timeOnLetter*1000);                ///< Setting the delay on the time on letter timer.
      timerOnLetter.enable();                                   ///< Resetting the time on letter timer.
      timerDone = false;                                        ///< Dropping the timerDone flag.
    }
    /** The next section is executed if the state of the Arduino isn't ready to read.
     */
    else
    {
      shouldRead = READY_TO_READ;                               ///< Setting the Arduino's state to ready to read.
    }
  }
  /** The next commands updates the running timers.
   */
  timerSendMsg.update();
  timerOnLetter.update();
  delay(LOOP_DELAY);                                            ///< loop delay to cool down the processor and control the communication rate.
}
/** @fn void loop()
 * @brief This function is the main loop executed by the Arduino.
 * @return This function doesn't return (void).
 */

void sendTimerCallback(){shouldSend = true;}
/** @fn void sendTimerCallback()
 * @brief This function is executed when the communication sender timer is over.
 * @return This function doesn't return (void).
 */
void resetTimer(){timerDone = true;}                      ///< This function is executed when the time on letter timer is over.
/** @fn void resetTimer()
 * @brief This function is executed when the time on letter timer is over.
 * @return This function doesn't return (void).
 */