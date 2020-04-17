#if !defined(COMMUNICATIONARDUINO)
#define COMMUNICATIONARDUINO

#include <Arduino.h>
#include <ArduinoJson.h>

class CommunicationArduino
{
public:
    CommunicationArduino()
    {

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

    void readCommand(int *command, int *purpose, int *time)
    {
        // Lecture du message Json
        StaticJsonDocument<500> doc;
        JsonVariant parse_msg;
        int newCommand = toAscii(' ');
        String currentPurpose = "none";
        int currentPurposeInt = 3;
        int timeOnLetter = 2;

        // Lecture sur le port Seriel
        DeserializationError error = deserializeJson(doc, Serial);

        // Si erreur dans le message
        if (error) {
            *command = newCommand;
            *purpose = 3;
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
            currentPurposeInt = 1;
        }
        else if(currentPurpose == "quiz")
        {
            currentPurposeInt = 2;
        }
        else
        {
            currentPurposeInt = 3;
        }
        
        *command = newCommand;
        *purpose = currentPurposeInt;
        *time = timeOnLetter;

        return;
    };
};

#endif // COMMUNICATIONARDUINO
