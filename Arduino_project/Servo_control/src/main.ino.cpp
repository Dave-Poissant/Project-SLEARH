# 1 "c:\\users\\davep\\appdata\\local\\temp\\tmpcfedd9"
#include <Arduino.h>
# 1 "C:/Users/davep/Unisherbrooke/Session4/Projet/Project-SLEARH/Arduino_project/Servo_control/src/main.ino"
#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <CommunicationArduino.h>
#include "SoftTimer/SoftTimer.h"
#include "Servo.h"


#define NOT_READY_TO_SEND false
#define READY_TO_SEND true
#define NOT_READY_TO_READ false
#define READY_TO_READ true

#define SEND_UPDATE_PERIODE 200
#define READ_UPDATE_PERIODE 1000
#define BAUD 9600
#define LOOP_DELAY 500


void sendTimerCallback();
void readTimerCallback();



CommunicationArduino comObject = CommunicationArduino();
volatile bool shouldSend = NOT_READY_TO_SEND;
volatile bool shouldRead = NOT_READY_TO_READ;
bool messageReceived = false;
SoftTimer timerSendMsg;
SoftTimer timerReadMsg;


Servo servo;


bool newCommand = false;
bool blinkState = false;
int increment = 0;
int command = ' ';
void setup();
void loop();
#line 43 "C:/Users/davep/Unisherbrooke/Session4/Projet/Project-SLEARH/Arduino_project/Servo_control/src/main.ino"
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(BAUD);
# 56 "C:/Users/davep/Unisherbrooke/Session4/Projet/Project-SLEARH/Arduino_project/Servo_control/src/main.ino"
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);
}







void loop() {
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

  delay(LOOP_DELAY);
}

void sendTimerCallback(){shouldSend = true;}
void readTimerCallback(){shouldRead = true;}