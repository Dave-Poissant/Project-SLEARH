#if !defined(SERVO)
#define SERVO

#include <Arduino.h>
#include <Adafruit_PWMServoDriver.h>

// Section to change when adding servos or characters:
#define NB_LETTERS            32                          //Number of characters managed
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

#define NOT_INCLINED          50                          //Angle for a straigth finger
#define INCLINED              150                         //Angle for an inclined finger

#define width                 2                           //Constante. 
#define MIN_PULSE_WIDTH       650
#define MAX_PULSE_WIDTH       2350
#define DEFAULT_PULSE_WIDTH   1500
#define FREQUENCY             50

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();    // Setting up the pwm object with the default address for the driver (0x40)
uint8_t servonum = 1;                                       // twelve servo objects can be created on most boards
                                                            // our servo # counter:

// Creating a structure for every character:
struct character{
  int id;
  int pattern[NB_FINGERS];
  int angle[NB_FINGERS];
} charact[NB_LETTERS];

class Servo
{
private:
    int lastCommand;
public:
    Servo(){
        int lastCommand = ' ';
        // Defining every character with the dedicated structure.
        charact[0] = {('0'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[1] = {('1'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[2] = {('2'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[3] = {('3'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[4] = {('4'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,VERTICAL,VERTICAL}};
        charact[5] = {('5'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,VERTICAL,VERTICAL}};
        charact[6] = {('a'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[7] = {('b'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{HORIZONTAL,VERTICAL,VERTICAL,VERTICAL,VERTICAL}};
        charact[8] = {('c'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{A90_DEGREE,A90_DEGREE,A90_DEGREE,A90_DEGREE,A90_DEGREE}};
        charact[9] = {('d'),{INDEX,MIDDLE,RING,LITTLE,THUMB},{VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[10] = {('e'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[11] = {('f'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{A90_DEGREE,A90_DEGREE,VERTICAL,VERTICAL,VERTICAL}};
        charact[12] = {('g'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[13] = {('h'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[14] = {('i'),{INDEX,MIDDLE,RING,LITTLE,THUMB},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,VERTICAL,FULLY_INCLINED}};
        charact[15] = {('j'),{INDEX,MIDDLE,RING,LITTLE,THUMB},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,VERTICAL,FULLY_INCLINED}};
        charact[16] = {('k'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[17] = {('l'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[18] = {('m'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[19] = {('n'),{LITTLE,RING,THUMB,INDEX,MIDDLE,},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[20] = {('o'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{A90_DEGREE,A90_DEGREE,A90_DEGREE,A90_DEGREE,A90_DEGREE}};
        charact[21] = {('p'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[22] = {('q'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[23] = {('r'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[24] = {('s'),{INDEX,MIDDLE,RING,LITTLE,THUMB},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED}};
        charact[25] = {('t'),{INDEX,MIDDLE,RING,LITTLE,THUMB},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,VERTICAL}};
        charact[26] = {('u'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[27] = {('v'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{FULLY_INCLINED,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[28] = {('w'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,VERTICAL,VERTICAL,FULLY_INCLINED,FULLY_INCLINED}};
        charact[29] = {('x'),{LITTLE,RING,MIDDLE,INDEX,THUMB},{FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,A90_DEGREE,FULLY_INCLINED}};
        charact[30] = {('y'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,VERTICAL}};
        charact[31] = {('z'),{THUMB,INDEX,MIDDLE,RING,LITTLE},{VERTICAL,FULLY_INCLINED,FULLY_INCLINED,FULLY_INCLINED,VERTICAL}};
    }

    bool servoOut(int character, int increment){
        character = adjustCommand(character);
        int finger = charact[character].pattern[increment];
        int moveOption = VERTICAL;
        moveFinger(finger,moveOption);
        lastCommand = character;
        if(increment < NB_FINGERS-1){return false;}
        else{return true;}
    }

    bool reverseMove(int character, int decrement){
        character = adjustCommand(character);
        int finger = charact[character].pattern[decrement];
        int moveOption = charact[character].angle[decrement];
        moveFinger(finger,moveOption);
        lastCommand = character;
        if(decrement > 0){return false;}
        else{return true;}
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
        int adjustedCommand = ' ';
        bool found = false;
        if(command <=53 && command >= 48){
            adjustedCommand = command - 48;
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
        /*
        for(int i=0;i<NB_FINGERS; i++){
            //pwm.setPWM(i, 0, pulseWidth(50));
            servoOut('b',i);
            delay(100);
        }
        */
        //servoOut('5');
        
        for(int i=0;i<1;i++){
            int command = charact[i].id;
            for(int increment=0;increment<NB_FINGERS; increment++){
                servoOut(command,increment);
                delay(200);
            }
            delay(1500);
            for(int decrement=NB_FINGERS-1;decrement>0; decrement--){
                reverseMove(command,decrement);
                delay(200);
            }
            delay(1000);
            Serial.println(command);
            Serial.println(charact[i].id);
            Serial.println("");
            //servoOut(adjustedCommand,0);
        }
        
        return testResult;
    }
};

#endif
