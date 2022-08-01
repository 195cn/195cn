import time
from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
import ntc

# hardware set
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)
adc = ADC(Pin(26))

R1M = 1000000
R100K = 100000
R10K = 10000
R1K = 1000

IO_R1M = 21
IO_R100k = 20
IO_R10k = 19
IO_R1K = 18

LIMIT_UP = 2217
LIMIT_LOW = 515


def adc2voltage(adc_value):
    voltage = adc_value * 3300 / 65535
    return int(voltage)


def adc2res(adc_value, reference_res):
    res = int(adc_value / (65535 - adc_value) * reference_res)
    return res


def lcd_init():
    oled.fill(0)
    oled.text("Ohmu Meter", 5, 5)
    oled.show()


def res_check_task():
    # 1M
    pin_R1M = Pin(IO_R1M, Pin.OUT)
    pin_R100k = Pin(IO_R100k, Pin.IN)
    pin_R10k = Pin(IO_R10k, Pin.IN)
    pin_R1K = Pin(IO_R1K, Pin.IN)

    pin_R1M.high()

    adc_value = adc.read_u16()
    voltage = adc2voltage(adc_value)
    print("1M" + str(voltage))

    if voltage > LIMIT_UP:
        return "HIGH LIMIT"

    if voltage > LIMIT_LOW:
        resistor = adc2res(adc_value, R1M)
        return resistor

    # 100K
    pin_R1M = Pin(IO_R1M, Pin.IN)
    pin_R100k = Pin(IO_R100k, Pin.OUT)

    pin_R100k.high()

    adc_value = adc.read_u16()
    voltage = adc2voltage(adc_value)
    print("100K" + str(voltage))

    if voltage > LIMIT_LOW:
        resistor = adc2res(adc_value, R100K)
        return resistor

    # 10K
    pin_R100k = Pin(IO_R100k, Pin.IN)
    pin_R10k = Pin(IO_R10k, Pin.OUT)

    pin_R10k.high()

    adc_value = adc.read_u16()
    voltage = adc2voltage(adc_value)
    print("10K" + str(voltage))

    if voltage > LIMIT_LOW:
        resistor = adc2res(adc_value, R10K)
        return resistor

    # 1K
    pin_R10k = Pin(IO_R10k, Pin.IN)
    pin_R1K = Pin(IO_R1K, Pin.OUT)

    pin_R1K.high()

    adc_value = adc.read_u16()
    voltage = adc2voltage(adc_value)
    print("1K" + str(voltage))

    if voltage < LIMIT_LOW:
        return "LOW LIMIT"

    if voltage > LIMIT_LOW:
        resistor = adc2res(adc_value, R1K)
        return resistor


def NTC_cal(ohum):
    pass


def main():
    # adc_task()
    # i2c_task()

    lcd_init()

    while True:

        ohum = res_check_task()

        oled.fill_rect(0, 15, 128, 17, 0)
        oled.text("Ohum:" + str(ohum), 5, 15)
        oled.show()

        temperature = ntc.ohum2temperature(ohum)

        oled.text("Temp:" + str(temperature) + " C", 5, 24)
        oled.show()


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
