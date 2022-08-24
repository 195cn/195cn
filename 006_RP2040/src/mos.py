
from machine import Pin, I2C, PWM, Timer
import time
from ssd1306 import SSD1306_I2C

mos_0 = Pin(20, Pin.OUT)
mos_1 = Pin(21, Pin.OUT)

button_0 = Pin(0, Pin.IN)
button_1 = Pin(1, Pin.IN)
button_2 = Pin(2, Pin.IN)

i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)

duty_list = [0, 32768, 65535]
duty_num = len(duty_list)
duty_index = 0

pwm_0 = PWM(mos_0)
pwm_0.freq(1000)
pwm_0.duty_u16(duty_list[duty_index])

pwm_1 = PWM(mos_1)
pwm_1.freq(1000)
pwm_1.duty_u16(duty_list[duty_index])


def lcd_init():

    oled.fill(0)
    oled.text("MOS PWM CONTROL", 5, 5)
    oled.show()


def main():

    global duty_index
    lcd_init()

    oled.fill_rect(0, 15, 128, 17, 0)
    oled.text("Duty:" + str(duty_list[duty_index]), 5, 15)
    oled.show()

    while True:
        if button_0.value() == 0:
            print("Button Down")
            duty_index += 1
            if duty_index == duty_num:
                duty_index = 0

            pwm_0.duty_u16(duty_list[duty_index])
            pwm_1.duty_u16(duty_list[duty_index])

            oled.fill_rect(0, 15, 128, 17, 0)
            oled.text("Duty:" + str(duty_list[duty_index]), 5, 15)
            oled.show()
            time.sleep(1)

        time.sleep_ms(50)
