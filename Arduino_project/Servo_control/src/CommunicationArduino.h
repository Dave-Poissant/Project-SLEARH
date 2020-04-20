/** @file CommunicationArduino.h
 * The file CommunicationArduino.h contains the class CommunicationArduino.
 */
#if !defined(COMMUNICATIONARDUINO)
#define COMMUNICATIONARDUINO

#include <Arduino.h>
#include <ArduinoJson.h>

class CommunicationArduino
{
    /** @class CommunicationArduino 
     * @brief Class containing functions related to the serial communication of the arduino.
     *
     * This class contains the functions used to send information through serial port and read some.
     * @author POISSANT, DAVID-ALEXANDRE
     * @date 19/04/2020
     */
public:
    CommunicationArduino()
    {
        /** @brief Default constructor for the object servo.
         * 
         */
    };

    void sendState(bool state)
    {
        /* Envoit du message Json sur le port seriel */
        StaticJsonDocument<500> doc;
        // Elements du message

        doc["com_state"] = state;

        // Serialisation
        serializeJson(doc, Serial);
        // Envoit
        Serial.println();
    };
    /** @fn void sendState(bool state)
     * @brief Function of the CommunicationArduino class. This function sends through the serial port the state in param.
     * @param state bool The state be send.
     */

    void readCommand(int *command, int *purpose, int *time)
    {
        // Lecture du message Json
        StaticJsonDocument<500> doc;
        JsonVariant parse_msg;
        int newCommand = toAscii(' ');
        String currentPurpose = "none";
        int currentPurposeInt = 2;
        int timeOnLetter = 2;

        // Lecture sur le port Seriel
        DeserializationError error = deserializeJson(doc, Serial);

        // Si erreur dans le message
        if (error) {
            *command = newCommand;
            *purpose = currentPurposeInt;
            *time = timeOnLetter;
            return;
        }
        // digitalWrite(LED_BUILTIN, LOW);

        // Analyse des éléments du message message
        parse_msg = doc["command"];
        if(!parse_msg.isNull()){
            newCommand = doc["command"].as<int>();
            currentPurpose = doc["purpose"].as<String>();
            timeOnLetter = doc["time"].as<int>();
        }

        if(currentPurpose == "educ")
        {
            currentPurposeInt = 0;
        }
        else if(currentPurpose == "quiz")
        {
            currentPurposeInt = 1;
        }
        else
        {
            currentPurposeInt = 2;
        }
        
        *command = newCommand;
        *purpose = currentPurposeInt;
        *time = timeOnLetter;

        return;
    };
    /** @fn void readCommand(int *command, int *purpose, int *time)
     * @brief Function of the CommunicationArduino class. This function reads the serial port for incoming commands.
     * @param command int* The "command" variable's adress in main.ino.
     * @param purpose int* The "purpose" variable's adress in main.ino.
     * @param time int* The "time" variable's adress in main.ino.
     */
};

#endif // COMMUNICATIONARDUINO
