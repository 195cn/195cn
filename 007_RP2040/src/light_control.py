import time
from machine import  PWM, ADC, Pin, I2C
from ssd1306 import SSD1306_I2C

# hardware set
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)

def lcd_init():
    oled.fill(0)
    oled.text("WS2812 Control", 5, 5)
    oled.show()







def main():
    lcd_init()

    while True:

        print("loop")    
        time.sleep(5)

    pass