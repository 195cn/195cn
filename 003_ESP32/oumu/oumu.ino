#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

// I2C
#define I2C_SDA 4
#define I2C_SCL 5

#define OHM_1M_PIN 15
#define OHM_100K_PIN 14
#define OHM_10K_PIN 13
#define OHM_1K_PIN 12

#define OHM_1M 1005000
#define OHM_100K 101100
#define OHM_10K 9860
#define OHM_1K 998

#define ADC_PIN 2

#define READTIME 10

int ohm_val = 0;

void setup()
{
    Serial.begin(115200);

    pinMode(OHM_1M_PIN, INPUT);
    pinMode(OHM_100K_PIN, INPUT);
    pinMode(OHM_10K_PIN, INPUT);
    pinMode(OHM_1K_PIN, INPUT);
    pinMode(ADC_PIN, INPUT);

    // LCD
    Wire.begin(I2C_SDA, I2C_SCL);
    // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    { // Address 0x3C for 128x32
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ; // Don't proceed, loop forever
    }

    display.clearDisplay();

    display.setTextSize(2);              // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0, 0);             // Start at top-left corner
    display.println(F("Ohm Meter"));
    display.display();
    delay(2000);
}

void loop()
{
    read_ohm();
    delay(1000);
}

void ohm_display(int ohm)
{
    String msg = "";

    if (ohm > 10000)
    {
        msg += ohm / 1000;
        msg += " K";
    }
    else
    {
        msg = ohm;
    }

    display.clearDisplay();

    display.setTextSize(2);              // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0, 0);             // Start at top-left corner
    display.println(msg);
    display.display();
}

void outline_display(int num)
{
    display.clearDisplay();

    display.setTextSize(2);              // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0, 0);             // Start at top-left corner
    if (num == 0)
        display.println("< 100 ohm");
    else
        display.println("> 2M ohm");
    display.display();
}

void read_ohm()
{
    int temp = 0;

    // 1M
    pinMode(OHM_1M_PIN, OUTPUT);
    pinMode(OHM_100K_PIN, INPUT);
    pinMode(OHM_10K_PIN, INPUT);
    pinMode(OHM_1K_PIN, INPUT);

    digitalWrite(OHM_1M_PIN, HIGH);
    // digitalWrite(ADC_PIN, LOW);
    delay(READTIME);
    temp = adc_fliter(ADC_PIN);

    if (temp < 384)
    {
        ;
    }
    else if (temp > 2950)
    {
        outline_display(1);
        return;
    }
    else
    {
        ohm_val = cal_ohm(temp, OHM_1M);
        Serial.printf("%s OHM:%d\n", "1M", ohm_val);
        ohm_display(ohm_val);
        return;
    }

    // 100K
    pinMode(OHM_1M_PIN, INPUT);
    pinMode(OHM_100K_PIN, OUTPUT);
    pinMode(OHM_10K_PIN, INPUT);
    pinMode(OHM_1K_PIN, INPUT);

    digitalWrite(OHM_100K_PIN, HIGH);
    delay(READTIME);
    temp = adc_fliter(ADC_PIN);

    if (temp < 384)
    {
        ;
    }
    else
    {

        ohm_val = cal_ohm(temp, OHM_100K);
        Serial.printf("%s OHM:%d\n", "100K", ohm_val);
        ohm_display(ohm_val);
        return;
    }

    // 10K
    pinMode(OHM_1M_PIN, INPUT);
    pinMode(OHM_100K_PIN, INPUT);
    pinMode(OHM_10K_PIN, OUTPUT);
    pinMode(OHM_1K_PIN, INPUT);

    digitalWrite(OHM_10K_PIN, HIGH);
    delay(READTIME);
    temp = adc_fliter(ADC_PIN);

    if (temp < 384)
    {
        ;
    }
    else
    {
        ohm_val = cal_ohm(temp, OHM_10K);
        Serial.printf("%s OHM:%d\n", "10K", ohm_val);
        ohm_display(ohm_val);
        return;
    }

    // 1K
    pinMode(OHM_1M_PIN, INPUT);
    pinMode(OHM_100K_PIN, INPUT);
    pinMode(OHM_10K_PIN, INPUT);
    pinMode(OHM_1K_PIN, OUTPUT);

    digitalWrite(OHM_1K_PIN, HIGH);
    delay(READTIME);
    temp = adc_fliter(ADC_PIN);

    if (temp < 384)
    {
        outline_display(0);
        return;
    }
    else
    {
        ohm_val = cal_ohm(temp, OHM_1K);
        Serial.printf("%s OHM:%d\n", "1K", ohm_val);
        ohm_display(ohm_val);
        return;
    }
}

int cal_ohm(int adc, int r0)
{
    return (int)(adc / (4095.0 - adc) * r0);
}

int adc_fliter(int pin)
{
    int temp = 0;
    int voltag = 0;

    for (int i = 0; i < 5; i++)
    {
        temp += analogRead(pin);
        delay(10);
    }

    temp = temp / 5 + 180;
    voltag = map(temp, 0, 4096, 0, 3300);
    Serial.printf("[analogRead]ADC:%d VOL:%d\n", temp, voltag);

    return temp;
}