# 起因

最近重启了PCB画板的学习项目，计划系统的学一下电子电路，补充单片机方面的短板。搞了两年多单片机软件了，因为不会设计电路，很多项目被迫放弃。
因为含贴片对我来说有些难度，而我的目标产品对体积没有要求，后续不出意外都是用插接件。而且前期熟悉并学习常见电路，基本是用洞洞板来测试的，比如三极管，MOS管，RC电路等。
这就引出了一个问题：我TM是个色盲，我无法分辨电阻色环。
于是在项目开始，先打算做一个简单的自动档欧姆表，方便快速测量阻值。正好公司有自己的产品，带I2C屏幕的ESP32，能用就直接用嘛，做一个简单的扩展板。

# 目标：

测量100Ω到10MΩ的电阻，只大概定性，不做精度要求。

- ESP32单片机
- SSD1306屏幕
- 12bit ADC

# 原理解析

整体上是一个分压的原理，R0是已知电阻，R是待测电阻，A是ADC测试点，画的比较潦草。
A点测R两端电压，VCC为3.3V，x是ADC度数，12bit ADC的范围是0~4095，公式还是比较好理解的。
​![](https://pic3.zhimg.com/80/v2-ce985f2c00c3e6d8582f6e9f3b60dc6a_720w.jpg)

可以得出 R/R0 = f(ADC)，以及反函数。这里最开始没想明白ADC精度和阻值范围的关系。
​

最开始我是去直接看y=x/(4096-x)的函数图像的，只看图很难分析个所以然。

添加图片注释，不超过 140 字（可选）
x就是ADC的值，我做了一个表格，看起来更清晰一点。
​

可以看出来ADC为2048的时候，也就是R == R0，分压1.67V，以这个为分界线。
ADC 384~2048，R/R0的的范围为0.1~1
ADC 2048~3712，R/R0的的范围为1~9.67
所以尽量保持R0在待测电阻R的10倍范围内，精度相对会高一点，所以我拟定了4个电阻值：

- 1k
- 10k
- 100k
- 1M

基本能覆盖到100Ω~10MΩ，足够我平时使用了，超过范围的还是用万用表。
电路设计
电路很简单，我大概用立创EDA摆了一下就直接焊洞洞板了，没有做面包板验证。
​

# PCB焊接

手里没有5P的排母，直接剪了一个16P的，问题不大。
​

# ESP32 ADC误差

额，ADC读取有误差，用10K电阻测试，ADC应该在2048左右，但在1840左右浮动。ADC转换成欧姆以后只有8K左右。经过排查发现，Arduino下的ADC读取约有80%到90%的误差，而且非线性。
​

考虑把ADC读取的部分换成ESP-IDF的原生API，并且把测量范围降低。我猜测是ADC衰减导致的问题，默认应该是ADC_ATTEN_DB_11。
由于公司最近有产品是基于ESP32测量ADC来工作的，和同事反映了一下这个问题，领导让我列个表：

​

| 实测电压mv | 理论ADC | 实际ADC | 换算电压 | ADC插值 | 电压差值 |
| ------ | ----- | ----- | ---- | ----- | ---- |
| 0      | 0     | 0     | 0    | 0     | 0    |
| 96     | 119   | 0     | 0    | 119   | 96   |
| 150    | 186   | 48    | 38   | 138   | 112  |
| 193    | 240   | 99    | 79   | 141   | 114  |
| 254    | 315   | 173   | 139  | 142   | 115  |
| 303    | 376   | 234   | 188  | 142   | 115  |
| 314    | 390   | 243   | 195  | 147   | 119  |
| 398    | 494   | 344   | 277  | 150   | 121  |
| 499    | 619   | 464   | 373  | 155   | 126  |
| 599    | 743   | 591   | 476  | 152   | 123  |
| 701    | 870   | 715   | 576  | 155   | 125  |
| 895    | 1111  | 958   | 771  | 153   | 124  |
| 1000   | 1241  | 1092  | 879  | 149   | 121  |
| 1302   | 1616  | 1457  | 1173 | 159   | 129  |
| 1604   | 1991  | 1833  | 1476 | 158   | 128  |
| 1994   | 2475  | 2305  | 1857 | 170   | 137  |
| 2199   | 2729  | 2551  | 2060 | 178   | 139  |
| 2399   | 2978  | 2810  | 2263 | 168   | 136  |
| 2603   | 3231  | 3082  | 2483 | 149   | 120  |
| 2805   | 3482  | 3404  | 2740 | 78    | 65   |
| 3104   | 3853  | 4095  | 3299 | -242  | -195 |

目前来看，在默认的ADC_ATTEN_DB_11衰减时，电压在200mv到2400mv间，有大概-110mv到-140mv的误差。换算成ADC差值约为148.94，我直接在读ADC后加上150，现在换算出来的结果和实际测量基本一致。
ESP-IDF原生的API和Arduino的analogyRead结果一致，算是解决了问题。
但由于有效范围变小了，导致原来欧姆表的测量范围也有变化。目前的ADC有效值的范围是170~2800，补上ADC的偏移误差150就是320~2950。根据之前的表格，测量范围缩减到100Ω~2MΩ，仍然满足使用要求。

# 最终版本

家里没有多余电位器了，没有对家里的ESP32进行再次校准，把ADC偏移补偿了大概180，结果才大致相同。
我很不满意这个结果，目前看来可以凑合用。手里还有一个Arduino Nano，准备等购买的屏幕到货以后再做一个Nano版本的，这个就这样吧。

代码上传到了Github留档，到时候改一下Pin就可以了。