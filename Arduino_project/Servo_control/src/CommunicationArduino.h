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

    String readCommand()
    {
        // Lecture du message Json
        StaticJsonDocument<500> doc;
        JsonVariant parse_msg;
        int newCommand = toAscii(' ');
        String currentPurpose = "none";
        int timeOnLetter = 2;

        // Lecture sur le port Seriel
        DeserializationError error = deserializeJson(doc, Serial);

        // Si erreur dans le message
        if (error) {
            return String(newCommand) + "|" + "none" + "|" + String(timeOnLetter);
        }
        // digitalWrite(LED_BUILTIN, LOW);

        // Analyse des éléments du message message
        parse_msg = doc["command"];
        if(!parse_msg.isNull()){
            newCommand = doc["command"].as<int>();
            currentPurpose = doc["purpose"].as<String>();
            timeOnLetter = doc["time"].as<int>();
        }

        String returnValue = String(toAscii(newCommand)) + "|" + currentPurpose + "|" + String(timeOnLetter);

        return returnValue;
    };
};

#endif // COMMUNICATIONARDUINO
