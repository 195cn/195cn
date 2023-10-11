#include <Adafruit_NeoPixel.h>

#define DELAYVAL 10

Adafruit_NeoPixel ws_0(30, 0, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel ws_1(144, 1, NEO_GRB + NEO_KHZ800);

void setup()
{
    Serial.begin(115200);
    ws_1.begin();
}

void loop()
{
    Serial.println("loop");

    for (int i = 0; i < 142; i++)
    {
        if (i < 28)
        {
            ws_0.setPixelColor(i, ws_1.Color(255, 255, 255));
            ws_0.show();
        }

        ws_1.setPixelColor(i, ws_1.Color(255, 255, 255));
        ws_1.show();
        delay(DELAYVAL);
    }

    delay(5000);

    for (int i = 0; i < 144; i++)
    {
        if (i < 30)
        {
            ws_0.setPixelColor(i, ws_1.Color(0, 0, 0));
            ws_0.show();
        }

        ws_1.setPixelColor(i, ws_1.Color(0, 0, 0));
        ws_1.show();

        delay(DELAYVAL);
    }

    delay(3000);
}