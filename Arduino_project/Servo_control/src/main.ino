#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <CommunicationArduino.h>
#include "SoftTimer/SoftTimer.h"

// Section to change when adding servos or characters:
#define NB_LETTERS            6                           //Number of letters managed
#define NB_MOTORS             10                          // Number of active motors
#define NB_FINGERS            5                           // Number of active fingers

// The next defined are the different articulated positions for a finger:
#define VERTICAL              0
#define HORIZONTAL            1
#define A90_DEGREE            2
#define FULLY_INCLINED        3                           //Value obtained from testing

// The next defined are the diffrent finger implemented:
#define THUMB                 0
#define INDEX                 2
#define MIDDLE                4
#define RING                  6
#define LITTLE                8

// The next defined are the different communication states:
#define NOT_READY_TO_SEND     false
#define READY_TO_SEND         true
#define NOT_READY_TO_READ     false
#define READY_TO_READ         true

#define SEND_UPDATE_PERIODE   200                         // sent of Read state Periode (ms)
#define READ_UPDATE_PERIODE   1000                        // read of Serial Periode (ms)
#define BAUD                  9600                        // Baud rate for Arduino mega 2560

#define NOT_INCLINED          25                          //Angle for a straigth finger
#define INCLINED              140                         //Angle for an inclined finger

#define width                 2                           //Constante. 
#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50


// ----------------------------- Function prototypes ---------------------------------

void sendTimerCallback();                                 // callback to update the send Serial.read state
void readTimerCallback();                                 // callback to update the send Serial.read state

int servoOut(int character);
int moveFinger(int finger, int moveOption);

int pulseWidth(int angle);

int adjustCommand(int command);

int test();

// ------------------------------- Other variables -----------------------------------
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();  // Setting up the pwm object with the default address for the driver (0x40)

// Communication variables:
CommunicationArduino comObject = CommunicationArduino();  // Only instance of CommunicationArduino class, to send and read from python UI
volatile bool shouldSend = NOT_READY_TO_SEND;             // flag to send a message
volatile bool shouldRead = NOT_READY_TO_READ;             // flag to read a message
bool messageReceived = false;                             // flag to show if the arduino as already received a message (temporary) 
SoftTimer timerSendMsg;                                   // send messages timer
SoftTimer timerReadMsg;                                   // read messages timer (temporary)

// twelve servo objects can be created on most boards
// our servo # counter:
uint8_t servonum = 1;

// command variables:
bool newCommand = false;                                  //Normaly initialized to 0. Set to 1 for testing purposes.
int lastCommand = ' ';
int command = ' ';
int adjustedCommand = ' ';

// Creating a structure for every character:
struct character{
  int id;
  int pattern[NB_FINGERS];
  int angle[NB_FINGERS];
} charact[NB_LETTERS];
// End of the section to change when adding servos or characters

bool blinkState = false;                                  // built-in LED's blinkState


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

  // Defining every character with the dedicated structure.
  charact[0] = {('0'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
  charact[1] = {('1'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
  charact[2] = {('2'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
  charact[3] = {('3'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
  charact[4] = {('4'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,VERTICAL,VERTICAL}};
  charact[5] = {('5'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,VERTICAL,VERTICAL}};
}

void loop() {

  if(shouldSend)
  {
    comObject.sendState(shouldRead);
  }

  if(shouldRead == NOT_READY_TO_READ){
    //adjustedCommand = adjustCommand(command);
    //test();
    //if(newCommand && adjustedCommand != ' '){
    //  newCommand = 0;
    //  servoOut(adjustedCommand);
    //}
  }

  if(shouldRead == READY_TO_READ){
    int newCommandInAscii = comObject.readCommand();
    if(newCommandInAscii == toAscii('a'))
    {
      shouldRead = NOT_READY_TO_READ;
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(newCommandInAscii == toAscii('b'))
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
  timerReadMsg.update();
  delay(FREQUENCY);
}

void sendTimerCallback(){shouldSend = true;}
void readTimerCallback(){shouldRead = true;}

int servoOut(int character){
  for(int j=0;j<NB_FINGERS; j++){
    int finger= charact[character].pattern[j];
    int moveOption = charact[character].angle[j];
    moveFinger(finger,moveOption);
    delay(500);
  }
  lastCommand = character;
  return 0;
}
int moveFinger(int finger, int moveOption){
  int nbMotor = 2;
  int angle[nbMotor];
  for(int i=0;i<nbMotor;i++){
    angle[i] = 25;
  }
  bool readyToMove = false;
  if(moveOption == 0){
    angle[0] = NOT_INCLINED;
    angle[1] = NOT_INCLINED;
    readyToMove = true;
  }
  if(moveOption == 1){
    angle[0] = INCLINED;
    angle[1] = NOT_INCLINED;
    readyToMove = true;
  }
  if(moveOption == 2){
    angle[0] = NOT_INCLINED;
    angle[1] = INCLINED;
    readyToMove = true;
  }
  if(moveOption == 3){
    angle[0] = INCLINED;
    angle[1] = INCLINED;
    readyToMove = true;
  }
  else{}
  if(readyToMove){
    for(int i=0; i<nbMotor; i++){
      //delay(500);
      pwm.setPWM(finger+i, 0, pulseWidth(angle[i]));
    }
  }
  return 0;
}

int pulseWidth(int angle){
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return analog_value;
}

int adjustCommand(int command){
  bool found = false;
  if(command <=53 && command >= 48){
    adjustedCommand = command-48;
    found = true;
  }
  if(command >= 97 && command <=122){
    adjustedCommand = command - 91;
    found = true;
  }
  if(!found){
    adjustedCommand = ' ';
  }
  return adjustedCommand;
}

int test(){
  bool testResult = 0;
  for(int i=0;i<NB_LETTERS;i++){
    command = charact[i].id;
    adjustedCommand = adjustCommand(command);
    servoOut(adjustedCommand);
  }
  return testResult;
}
