import math

# Nominal resistance at 25⁰C
nominal_resistance = 100000

# temperature for nominal resistance (almost always 25⁰ C)
nominal_temeprature = 25

# The beta coefficient or the B value of the thermistor (usually 3000-4000) check the datasheet for the accurate value.
beta = 3950

# Value of  resistor used for the voltage divider
Rref = 100000


def ohum2temperature(ohum):

    if isinstance(ohum,str):
        print("Input not num")
        return -999

    temperature = ohum / nominal_resistance  # (R/Ro)
    temperature = math.log(temperature)  # ln(R/Ro)
    temperature /= beta  # 1/B * ln(R/Ro)
    temperature += 1.0 / (nominal_temeprature + 273.15)  # + (1/To)
    temperature = 1.0 / temperature  # Invert
    temperature -= 273.15  # convert absolute temp to C

    print("Temperature " + str(temperature) + " C")
    return temperature
