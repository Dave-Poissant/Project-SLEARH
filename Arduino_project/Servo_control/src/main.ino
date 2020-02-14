#include <Arduino.h>
#include <Servo.h>
#include <string.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//Section to change when adding servos or characters
#define NB_LETTERS  2 //Number of letters managed
#define NB_MOTORS   4 // Number of active motors
#define NB_FINGERS  2 // Number of active fingers

//The next defined are the different articulated positions for a finger
#define VERTICAL              0
#define HORIZONTAL            1
#define NINETY_DEGREE         2
#define FULLY_INCLINED        3   //Value obtained from testing

//The next defined are the diffrent finger implemented
#define THUMB                 0
#define INDEX                 2
#define MIDLLE                4
#define RING                  6
#define LITTLE                8

//Creating arrays for every character
//Creating a pattern table for every character
int patternTable[NB_LETTERS][(NB_MOTORS*2)+1] = {       {int('0'),THUMB,FULLY_INCLINED,INDEX,FULLY_INCLINED},
                                                        {int('1'),THUMB,FULLY_INCLINED,INDEX,VERTICAL}
                                                                                                              };

//End of the section to change when adding servos or characters

#define NOT_INCLINED 140  //Angle for a straigth finger
#define INCLINED     25   //Angle for an inclined finger

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();  //Setting up the pwm object with the default address for the driver (0x40)

#define width 2 //Constante. 
#define BAUD 9600 // Baud rate for Arduino mega 2560
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

// twelve servo objects can be created on most boards

// our servo # counter
uint8_t servonum = 1;

//int pos = 0;    // variable to store the servo position
bool newCommand = true; //Normaly initialized to 0. Set to 1 for testing purposes.
int command = '1';
/*
struct character{
  int id;
  int pattern[NB_MOTORS];
  int angle[NB_MOTORS];
} nb0, nb1;
struct finger{  
  Servo proximal;
  Servo distal;
} index;
*/
void setup() {
  Serial.begin(BAUD);
  while(! Serial);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);  // Analog servos run at ~60Hz updates.

  //Setting string motor names to int values
  //indexProximal = 0;
  //indexDistal = 1;

  //Character * nb0 = new Character;
  //Character * nb1 = new Character;

  //nb0->set_values('0', int {0,1}, int{0,0}); 
}
int z = 0;
void loop() {
  
  //Section pour tests
  /*
  pwm.setPWM(1, 0, pulseWidth(140));
  delay(1000);
  pwm.setPWM(1, 0, pulseWidth(25));
  delay(1000);
  */
  /*
  index.proximal.write(140);
  index.distal.write(140);
  delay(1000);
  index.proximal.write(25);
  index.distal.write(25);
  delay(1000);
  */
  if(z%2 == 0){
    command = '0';
  }
  else{
    command = '1';
  }
  z++;
  newCommand = true;
  delay(3000);

  if(newCommand && command != ' '){
    Serial.println("New command && command != ' '.");
    newCommand = 0;
    servoOut(command);
  }
  delay(100);
}

int servoOut(int command){
  Serial.println("servoOut function.");
  for(int i=0;i<NB_LETTERS;i++){
    Serial.println(String("Command: ")+command);
    Serial.println(String("patternTable: ")+patternTable[i][0]);
    if(patternTable[i][0] == command){
      Serial.println("FOUND IN PATTERNTABLE");
      Serial.println(String("Command: ")+command);
      Serial.println(String("patternTable: ")+patternTable[i][0]);

      for(int j=0;j<NB_FINGERS*2; j+=2){
        Serial.println("IT'S A GO");
        int finger = patternTable[i][j+1];
        int moveOption = patternTable[i][j+2];
        Serial.println(String("FINGER : ")+finger);
        Serial.println(String("Move OPTION : ")+moveOption);
        moveFinger(finger,moveOption);
      }
    }
  }
  /*
  int pattern[NB_MOTORS];
  int angle[NB_MOTORS];
  if(command == 48){
    for(int i=0;i<NB_MOTORS; i++){
      pattern[i] = nb0.pattern[i];
      angle[i] = nb0.pattern[i];
      //Serial.println(pattern[i]);
    }
  }
  else if(command == 49){
    //pattern = nb1.pattern;
  }
  
  for(int i=0; i<NB_MOTORS; i++){
    pwm.setPWM(pattern[i], 0, pulseWidth(angle[i]));
    delay(500);
  }
  */
}
int moveFinger(int finger, int moveOption){
  Serial.println("moveFINGER");
  Serial.println(String("FINGER : ")+finger);
  Serial.println(String("Move OPTION : ")+moveOption);
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
    Serial.println("OPTION 3");
    angle[0] = INCLINED;
    angle[1] = INCLINED;
    readyToMove = true;
  }
  else{
    Serial.println("fuckkkkkkkkkk");
    //return 1;
  }
  if(readyToMove){
    Serial.println("READY TO MOVE");
    for(int i=0; i<nbMotor; i++){
      Serial.println(String("MOVING : ")+i);
      delay(500);
      pwm.setPWM(finger+i, 0, pulseWidth(angle[i]));
    }
  }
}

int pulseWidth(int angle){
  int pulse_wide, analog_value;
  pulse_wide   = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  analog_value = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  //Serial.println(analog_value);
  return analog_value;
}




