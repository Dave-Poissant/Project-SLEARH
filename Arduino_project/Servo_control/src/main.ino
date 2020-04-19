#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <CommunicationArduino.h>
#include "SoftTimer/SoftTimer.h"
#include "Servo.h"

// The next defined are the different communication states:
#define NOT_READY_TO_SEND     false
#define READY_TO_SEND         true
#define NOT_READY_TO_READ     false
#define READY_TO_READ         true

#define SEND_UPDATE_PERIODE   200                         // sent of Read state Periode (ms)
#define READ_UPDATE_PERIODE   1000                        // read of Serial Periode (ms)
#define BAUD                  9600                        // Baud rate for Arduino mega 2560
#define LOOP_DELAY            200                         // time delay between each finger mouvment
#define TIME_ON_LETTER        1000

#define EDUCATION             0
#define QUIZ                  1
#define UNFOUND               2

// ----------------------------- Function prototypes ---------------------------------
void sendTimerCallback();                                 // callback to update the send Serial.read state
void readTimerCallback();                                 // callback to update the send Serial.read state
void resetTimer();                                        // callback to reset time spend on letter

// ------------------------------- Other variables -----------------------------------
// Communication variables:
CommunicationArduino comObject = CommunicationArduino();  // Only instance of CommunicationArduino class, to send and read from python UI
volatile bool shouldSend = NOT_READY_TO_SEND;             // flag to send a message
volatile bool shouldRead = NOT_READY_TO_READ;             // flag to read a message
bool messageReceived = false;                             // flag to show if the arduino as already received a message (temporary) 
SoftTimer timerSendMsg;                                   // send messages timer
SoftTimer timerReadMsg;                                   // read messages timer (temporary)
SoftTimer timerOnLetter;                                  // Monitors the time spent on each letter before resetting to initial position

// Initiating the Servo class
Servo servo;

// command variables:
bool moveDone = false;                                    // Flag to control the main loop according to if the hand finished moving to the desired character
bool reverseDone = false;                                 // Flag to control the main loop according to if the hand finished moving back to it's initial position
bool newCommand = false;                                  // Normaly initialized to 0. Set to 1 for testing purposes.
bool blinkState = false;                                  // built-in LED's blinkState
int increment = 0;                                        // Increment to control which finger is it's turn to be moved
int decrement = NB_FINGERS-1;                             // Decrement to control which finger is it's turn to be moved back to initial position
int lastCommand = toAscii(' ');                           // Memorizing the last command achieved in this variable
int command = ' ';                                        // Memorizing the character to be displayed by the hand
int purpose = UNFOUND;                                    // Memorizing in which mode the application is used (Quiz or educationnal)
int timeOnLetter = 1;                                     // Memorizing the time that has to be spent on each letter
bool timerDone = false;                                   // Flag for the timer of the time spent on each letter


// -------------------------------------Setup----------------------------------------
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD);
  // Initializing the timer to send the state to the Pi
  timerSendMsg.setDelay(SEND_UPDATE_PERIODE);
  timerSendMsg.setCallback(sendTimerCallback);
  timerSendMsg.enable();
  // Initializing the timer to handle the time spent on each letter
  timerOnLetter.setDelay(TIME_ON_LETTER);
  timerOnLetter.setCallback(resetTimer);
  timerOnLetter.enable();
  // initializing the pwm
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);  // Analog servos run at ~60Hz updates. 
  // Placing every fingers to the initial position
  for(int increment = 0; increment<NB_FINGERS; increment++){
    servo.servoOut('5',increment);
  }
}

void loop() {
  if(shouldSend)
  {
    comObject.sendState(shouldRead);
  }

  if(shouldRead == NOT_READY_TO_READ){
    if(purpose != QUIZ){
      if(!moveDone && servo.servoOut(command,increment)){
        moveDone = true;
      }
      if(timerDone){
        if(moveDone && servo.reverseMove(command, decrement)){
          reverseDone = true;
          shouldRead = READY_TO_READ;
          increment = 0; 
          decrement = NB_FINGERS-1;
          lastCommand = command;
          command = ' ';
        }
      }
      if(!moveDone){increment++;}
      if(timerDone && moveDone && !reverseDone){decrement--;}
    }

    else if(purpose == QUIZ){
      if(lastCommand != toAscii(' ')){
        if(!reverseDone && servo.reverseMove(lastCommand, decrement)){
          reverseDone = true;
        }
        if(reverseDone && servo.servoOut(command, increment)){
          if(timerDone){
            moveDone = true;
            shouldRead = READY_TO_READ;
            increment = 0;
            decrement = NB_FINGERS-1;
            lastCommand = command;
            command = ' ';
          }
        }
      }
      if(!reverseDone){decrement--;}
      if(timerDone && reverseDone && !moveDone){increment++;}
    }
  }

  if(shouldRead == READY_TO_READ){
    moveDone = false;
    reverseDone = false;
    comObject.readCommand(&command, &purpose, &timeOnLetter);
    if(command != toAscii(' ')){
      shouldRead = NOT_READY_TO_READ;
      timerOnLetter.setDelay(timeOnLetter*1000);
      timerOnLetter.enable();
      timerDone = false;
    }
    /*
    if(command == toAscii('a'))
    {
      shouldRead = NOT_READY_TO_READ;
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(command == toAscii('b'))
    {
      shouldRead = NOT_READY_TO_READ;
      digitalWrite(LED_BUILTIN, LOW);
    }
    */
    else
    {
      shouldRead = READY_TO_READ;
    }
  }
  timerSendMsg.update();
  timerOnLetter.update();
  //timerReadMsg.update();
  delay(LOOP_DELAY);
}

void sendTimerCallback(){shouldSend = true;}
void resetTimer(){timerDone = true;}