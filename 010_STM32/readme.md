# STM32创建STM32CubeMX工程

基于正点原子教程
[【正点原子】手把手教你学STM32 HAL库开发全集【真人出镜】STM32入门教学视频教程 单片机 嵌入式](https://www.bilibili.com/video/BV1bv4y1R7dp?p=33&vd_source=3d7a183ebd9d40fbac41c2a6e4f25f74)

P33 第33讲，基础篇，新建STM32CubeMX工程

# 前期准备

准备好开发环境，安装STM32CubeMX。

固件包软件会自己下载，无需额外下载。


# 新建CubeMX项目

## 选择芯片

开始新MCU工程

搜索STM32F103ZET6，双击。

## 时钟

### 时钟源设置

选择System Core，选择RCC

HSE（高速外部时钟源）选择来自晶振

LSE（低速外部时钟源）选择来自晶振

### 时钟频率设置

HSE设置为8 MHz

LSE设置为32.768 KHz

PLL Source Mux （锁相环时钟源）选择来自外部晶振HSE

System Clock Mux（系统时钟源）选择来自锁相环的时钟PLLCLK

PLLMUL（锁相环倍频器）设置为9，获得72MHz的系统时钟。

APB1 Prescaler（APB总线分频器）设置为2，获得36MHz的总线时钟。


## PINOUT配置

### Pinout view

战舰开发板

LED0 PB5设置为GPIO_OUTPUT

LED1 PE5设置为GPIO_OUTPUT

### System view

进入GPIO设置

设置默认高电平，推挽输出，低速度，别名。

因为F1输出时没有上下拉，可以不用设置。

## 内核配置

选择System Core，选择SYS

Debug选择Serial Wire（SWD）

## 设置NVIC

Priority Group默认为4，视频说设置为2，实测有问题，保持默认。

## Project Manager

设置工程信息，最后选择GENERATE CODE输出代码。

### Project

设置工程名，设置保存路径。

ToolChain设置为MKD-ARM，版本V5。

### Code Generator

选择仅拷贝必要库。


# 添加逻辑代码

打开Keil项目,在/* USER 中间增加用户代码，防止被CubeMX覆盖。

```c
/* USER CODE BEGIN 3 */
    HAL_GPIO_TogglePin(LED0_GPIO_Port, LED0_Pin);
    HAL_GPIO_TogglePin(LED1_GPIO_Port, LED1_Pin);
    HAL_Delay(100);
/* USER CODE END 3 */
```

完成。