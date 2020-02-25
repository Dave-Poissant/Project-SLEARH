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
#define LOOP_DELAY            500                         // time delay between each finger mouvment

// ----------------------------- Function prototypes ---------------------------------
void sendTimerCallback();                                 // callback to update the send Serial.read state
void readTimerCallback();                                 // callback to update the send Serial.read state

// ------------------------------- Other variables -----------------------------------
// Communication variables:
CommunicationArduino comObject = CommunicationArduino();  // Only instance of CommunicationArduino class, to send and read from python UI
volatile bool shouldSend = NOT_READY_TO_SEND;             // flag to send a message
volatile bool shouldRead = NOT_READY_TO_READ;             // flag to read a message
bool messageReceived = false;                             // flag to show if the arduino as already received a message (temporary) 
SoftTimer timerSendMsg;                                   // send messages timer
SoftTimer timerReadMsg;                                   // read messages timer (temporary)

// Initiating the Servo class
Servo servo;

// command variables:
bool newCommand = false;                                  //Normaly initialized to 0. Set to 1 for testing purposes.
bool blinkState = false;                                  // built-in LED's blinkState
int increment = 0;
int command = ' ';


// -------------------------------------Setup ----------------------------------------
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD);

  timerSendMsg.setDelay(SEND_UPDATE_PERIODE);
  timerSendMsg.setCallback(sendTimerCallback);
  timerSendMsg.enable();

  timerReadMsg.setDelay(READ_UPDATE_PERIODE);
  timerReadMsg.setCallback(readTimerCallback);
  timerReadMsg.enable();

  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);  // Analog servos run at ~60Hz updates. 
}

void loop() {
  servo.test();
  if(shouldSend)
  {
    comObject.sendState(shouldRead);
  }

  if(shouldRead == NOT_READY_TO_READ){
    if(servo.servoOut(command,increment)){
      shouldRead = READY_TO_READ;
      increment = 0; 
      command = ' ';
    }
    //adjustedCommand = adjustCommand(command);
    //test();
    //if(newCommand && adjustedCommand != ' '){
    //  newCommand = 0;
    //  servoOut(adjustedCommand);
    //}
    else{increment++;}
  }

  if(shouldRead == READY_TO_READ){
    command = comObject.readCommand();
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
    else
    {
      shouldRead = READY_TO_READ;
    }
  }
  timerSendMsg.update();
  //timerReadMsg.update();
  delay(LOOP_DELAY);
}

void sendTimerCallback(){shouldSend = true;}
void readTimerCallback(){shouldRead = true;}