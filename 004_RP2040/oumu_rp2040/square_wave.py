from machine import Pin, I2C, PWM, Timer
import time
from ssd1306 import SSD1306_I2C

P_wave = Pin(15, Pin.OUT)
P22 = Pin(22, Pin.IN)

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)

freq_list = [200, 500, 1000, 2000, 5000, 10000]
# freq_list = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
freq_num = len(freq_list)
freq_index = 0

pwm = PWM(P_wave)
pwm.freq(freq_list[freq_index])
pwm.duty_u16(32768)


def lcd_init():

    oled.fill(0)
    oled.text("Square Wave", 5, 5)
    oled.show()


def main():

    global freq_index
    lcd_init()

    oled.fill_rect(0, 15, 128, 17, 0)
    oled.text("Freq:" + str(freq_list[freq_index]), 5, 15)
    oled.show()

    while True:
        if P22.value() == 0:
            print("Button Down")
            freq_index += 1
            if freq_index == freq_num:
                freq_index = 0

            pwm.freq(freq_list[freq_index])

            oled.fill_rect(0, 15, 128, 17, 0)
            oled.text("Freq:" + str(freq_list[freq_index]), 5, 15)
            oled.show()
            time.sleep(1)

        time.sleep_ms(50)
