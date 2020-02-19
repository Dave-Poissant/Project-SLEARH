#include <Arduino.h>
#include <string.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//Section to change when adding servos or characters
#define NB_LETTERS  6 //Number of letters managed
#define NB_MOTORS   10 // Number of active motors
#define NB_FINGERS  5 // Number of active fingers

//The next defined are the different articulated positions for a finger
#define VERTICAL              0
#define HORIZONTAL            1
#define A90_DEGREE            2
#define FULLY_INCLINED        3   //Value obtained from testing

//The next defined are the diffrent finger implemented
#define THUMB                 0
#define INDEX                 2
#define MIDDLE                4
#define RING                  6
#define LITTLE                8

#define NOT_READY             0
#define READY                 1

//Creating a structure for every character
struct character{
  int id;
  int pattern[NB_FINGERS];
  int angle[NB_FINGERS];
} charact[NB_LETTERS];

//End of the section to change when adding servos or characters

#define NOT_INCLINED 25  //Angle for a straigth finger
#define INCLINED     140   //Angle for an inclined finger

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();  //Setting up the pwm object with the default address for the driver (0x40)

#define width 2 //Constante. 
#define BAUD 9600 // Baud rate for Arduino mega 2560
#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

// twelve servo objects can be created on most boards
// our servo # counter
uint8_t servonum = 1;

bool newCommand = false; //Normaly initialized to 0. Set to 1 for testing purposes.
int lastCommand = ' ';
int command = ' ';
int adjustedCommand = ' ';

bool state = NOT_READY;


void setup() {
  //Serial.begin(BAUD);
  //while(! Serial);
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

  if(state == NOT_READY){
    adjustedCommand = adjustCommand(command);
    test();
    if(newCommand && adjustedCommand != ' '){
      newCommand = 0;
      servoOut(adjustedCommand);
    }

    state = READY;
    //sendState(state);
    delay(100);
  }

  if(state = READY){
    /*
    if(listen() == true){
      state = NOT_READY;
      sendState(state);
      commande = char;
      character to ascii
    }
    */
  }

}

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


