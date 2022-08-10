# 004 Pico自动档欧姆表(MicroPython平台)

# 起因

之前是先选用ESP32，因为公司大部分产品都是这个，也有两年的软件开发经验。但是处于对国产芯片的不信任，和一些使用过程不良体验，比如之前提到的ADC问题，就不考虑继续用了。我也基本不用联网相关的东西，主要做电机控制或者功率器件控制（3D打印相关），非要联网加个8266小板档AT模块用也没什么问题。

打算做个Arduino Nano的扩展版，后来考虑到ATMEGA328P的供货问题，以及这个老平台逐渐跟不上时代，决定直接转RP2040。公司近一年也做了三个RP2040的板，但是考虑到自己的水平，直接用了Pi Pico。

主要是RP2040好像是不自带flash，还有晶振之类乱七八糟的，外围电路我画PCB水平不够，先跳过。所以还是之前的原理，做一个自动挡的欧姆表。

![](https://pic2.zhimg.com/80/v2-f3eed7e309e3e29e67b5fe1b265670bd_720w.jpg)

# 原理解析

整体上是一个分压的原理，R0是已知电阻，R是待测电阻，A是ADC测试点，画的比较潦草。偷懒了就不重画了，具体的看之前的文章。。。

[狗脑：ESP32自动档欧姆表(Arduino平台)](https://zhuanlan.zhihu.com/p/540437244)

​![](https://pic3.zhimg.com/80/v2-ce985f2c00c3e6d8582f6e9f3b60dc6a_720w.jpg)

12bit ADC的范围是0~65535，这个和ESP32有点不一样。仍然是12bit，只是数值是16位的，所以转换公式要改一下。

# ADC测试

之前测ESP32之后就测过了，参见之前的文章：

[狗脑：RP2040 ADC精度测试（附ESP32对比）](https://zhuanlan.zhihu.com/p/542084789)

![](https://pic4.zhimg.com/80/v2-5c5e8651fdfc66a79f929e03712479e7_720w.jpg)

精度没有问题，而且是完整量程的，所以可以放心用，不用再考虑150mv到2450mv的区间，虽然之前的也大概够用。仍然使用1M，100K，10K，1K的电阻，从300mv（1：10）到3000mv（10：1），测量范围为100欧到10M欧。

# 电路设计

不仅仅是作为一个欧姆表，后续直接当开发板用，除了基本的ADC分压检测电路还扩展了一些东西：

- 3.3v，5v，GND引出
- I2C屏幕插座
- 复位按键
- 物理按键IO22

![](https://pic4.zhimg.com/80/v2-0ee52a5d5d2f118055acb21143e898d3_720w.jpg)

然后不太清楚AGND和GND的区别，做了一个跳冒，为了后面调试。

还有个bug不太明白原因，有的时候手持电阻或者杜邦线插进H1和H2的时候，会导致MCU重启。后面经测试，加了一个C1电容改善了很多。但由于模电知识匮乏，还不清楚原因。

嘛，整体上比较简单粗暴。

# PCB焊接

做了个60*60的板，并且画了外壳。目前还不打算做第二版，这个还是第一版没加电容的。完全依赖自动布线，然后后面手动的把5V和3.3V的线宽加粗了。。。我也是才发现RESET引脚饶了一大圈，不知道重启的问题和这个有没有关系。晶振我记得是要靠近MCU，不知道复位相关的东西要不要靠近。

![](https://pic1.zhimg.com/80/v2-d7ece77a31739876c42daf0c3ac4edcc_720w.jpg)

因为没用过其他的PCB绘制软件，比如AD啥的，我在公司完全不画板。也是头一次用立创EDA画PCB，大概一年还是两年前，跟着视频教程，大概画了一个51的板子，用的是老版本。这次用的专业版，挺好上手的，大概两三个小时就搞定了。

还有个小插曲就是，电阻的封装选错了，选了小一号的。但是不知道怎么批量修改电阻封装，结果就只能全部重新画一遍了。多亏了这个3D模拟，不然还真看不出来，而且焊盘感觉比公司同事画的要小，不知道如何调整。

然后有用自带的3D工具画了一个外壳，体验不错，之前试过导出DXF之类的格式再放到其他建模软件里画，很麻烦。

![](https://pic3.zhimg.com/80/v2-c4e4a35e6391312f2130f6059d63f37e_720w.jpg)

然后PCB是在嘉立创做的，22号下单，26号就收到了，还是挺快的，免费做了5块板。

# 代码

犹豫过用C SDK还是MicroPython，后来还是直接用MicroPython了，有一定开发经验，快又省事。。。我不推荐现在用RP2040的Arudino环境，官方有一个基于MBed的库，然后又有一个第三方的库，都不怎么好用。我不知道是我菜还是库的问题，SPI，I2C等引脚给限定死了，而且只能用一路。

其实还是挺想用Arduino的，库实在太多了。。。

![](https://pic3.zhimg.com/80/v2-d51dbb464887f0a9b9418b8b4c32bdda_720w.jpg)

虽然不像ESP32可以几乎任意重定义，但也是有好几组可以复用的，而Arduino比如SPI只能用16，17，18，19的样子，库源码里反正是这么写的。在公司做一个RP2040带SD卡和Lora的板子的时候遇到了这个问题，我和领导都没搞定就换成同一个硬件SPI，本来是想把两路SPI都用上的。

MicroPython提供了一个简单的SSD1306的库，比Arduino平台Adafruit的库差远了。这个是基于什么framebuf这个包的，但我Python不好没整明白。没有提供屏幕翻转，字体调整，画图也挺麻烦的。

核心代码放一下：

```python
# hardware set
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 32, i2c)
adc = ADC(Pin(26))

def adc2voltage(adc_value):
    voltage = adc_value * 3300 / 65535
    return int(voltage)

def adc2res(adc_value, reference_res):
    res = int(adc_value / (65535 - adc_value) * reference_res)
    return res
```

# 焊接 Debug

这焊盘太小了，真不好焊，我一开始以为复位问题是我虚焊导致的。后面单独焊了排母和复位按键，发现还有问题才考虑是不是没加电容的问题。

最开始没加C1电容，只有上拉。可能涉及到什么电路解耦的问题，印象中在某些视频里看过。

**总之，将就能用了。**

![](https://pic3.zhimg.com/80/v2-53d84c37bcf4cc1e360684376546921a_720w.jpg)

# NTC电阻测温

本质上这玩意也是测阻值，所以一起验证了。

代码是找了个Arduino代码抄的，公式没有详细考量过，不过应该问题不大。

```python
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
```

![](http://a1.qpic.cn/psc?/V11Sftcd4Zm0S7/ruAMsa53pVQWN7FLK88i5r2LeDlDaWR3UB2EUkZLfyENgY7J1MQrKHlifUr3.li2JmDfdffF.t0AxSv493KOezVHfIq5o*nUA9.ByL3TsAM!/c&ek=1&kp=1&pt=0&bo=gAegBYAHoAUWECA!&tl=3&vuin=1947356752&tm=1659387600&dis_t=1659389357&dis_k=7d034ae1700c3e53641d85aace1a1871&sce=60-2-2&rf=viewer_311)