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

    int readCommand()
    {
        // Lecture du message Json
        StaticJsonDocument<500> doc;
        JsonVariant parse_msg;
        int newCommand = toAscii(' ');

        // Lecture sur le port Seriel
        DeserializationError error = deserializeJson(doc, Serial);

        // Si erreur dans le message
        if (error) {
            return newCommand;
        }
        // digitalWrite(LED_BUILTIN, LOW);

        // Analyse des éléments du message message
        parse_msg = doc["command"];
        if(!parse_msg.isNull()){
            newCommand = doc["command"].as<int>();
        }

        return toAscii(newCommand);
    };
};

#endif // COMMUNICATIONARDUINO
