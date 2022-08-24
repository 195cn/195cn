import time
from machine import  PWM, ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
import ntc

# hardware set
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)

adc = ADC(Pin(26))
mos_0 = Pin(20, Pin.OUT)
mos_1 = Pin(21, Pin.OUT)

pwm_0 = PWM(mos_0)
pwm_0.freq(1000)
pwm_0.duty_u16(65535)

button_0 = Pin(0, Pin.IN)
button_1 = Pin(1, Pin.IN)
button_2 = Pin(2, Pin.IN)




def adc2voltage(adc_value):
    voltage = adc_value * 3300 / 65535
    return int(voltage)


def adc2res(adc_value, reference_res):
    res = int(adc_value / (65535 - adc_value) * reference_res)
    return res


def lcd_init():
    oled.fill(0)
    oled.text("Temper Control", 5, 5)
    oled.show()

#测电阻
def res_check_task():
    adc_value = adc.read_u16()
    voltage = adc2voltage(adc_value)
    resistor = adc2res(adc_value, 4700)

    return resistor

#测温任务
def temper_task():

    ohum = res_check_task()

    oled.fill_rect(0, 15, 128, 17, 0)
    oled.text("Ohum:" + str(ohum), 5, 15)
    oled.show()

    temperature = ntc.ohum2temperature(ohum)

    oled.text("Temp:" + str(temperature) + " C", 5, 24)
    oled.show()

    return temperature


def main():
    lcd_init()
    temper = 25.0

    while True:
        temper = temper_task()

        if(temper < 50):
            pwm_0.duty_u16(32768)
            mos_1.high()

        if(temper >52):
            pwm_0.duty_u16(65535)
            mos_1.low()
            
        time.sleep(1)

    pass


# main()

# def adc_task():
#     adc = ADC(Pin(26))
#     while True:
#         temp = adc.read_u16()
#         voltage = adc2voltage(temp)
#         print("ADC:" + str(temp) + "    VOL:" + str(voltage))
#         time.sleep(1)


# def i2c_task():
#     i2c = I2C(0, scl=Pin(17), sda=Pin(16))
#     # Display device address
#     print("I2C Address      : "+hex(i2c.scan()[0]).upper())
#     # Display I2C config
#     print("I2C Configuration: "+str(i2c))


# def read_res(reference_res):
#     adc_value = adc.read_u16()
#     voltage = adc2voltage(adc_value)
#     resistor = adc2res(adc_value, reference_res)
#     return voltage, resistor
