
from machine import  Pin
import time
import math
import array
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 10
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]


sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
sm.active(1)


def main():
    ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    
    for i in range(24):
        for j in range(NUM_LEDS):
            ar[j] >>= 1
        sm.put(ar, 8)
        time.sleep_ms(50)

    while True:
        

        print("blue")

        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j
            sm.put(ar,8)
            time.sleep_ms(5)

        print("RED")

        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<8
            sm.put(ar,8)
            time.sleep_ms(5)

        print("GREEN")
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<16
            sm.put(ar,8)
            time.sleep_ms(5)


if __name__ == "__main__":
    main()
