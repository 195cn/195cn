# STM32创建寄存器MDK工程

基于正点原子教程
[【正点原子】手把手教你学STM32 HAL库开发全集【真人出镜】STM32入门教学视频教程 单片机 嵌入式](https://www.bilibili.com/video/BV1bv4y1R7dp/?p=20&spm_id_from=333.880.my_history.page.click&vd_source=3d7a183ebd9d40fbac41c2a6e4f25f74)

P20 第20讲，基础篇，新建寄存器版本MDK工程

新建寄存器版本MDK工程步骤：

- 新建工程文件夹
- 新建工程框架
- 添加文件
- 魔术棒设置
- 添加用户代码

# 前期准备

准备好开发环境。

先下载固件包，固件包有一些 .c .h .s 文件。

固件包下载流程：

- 去www.st.com
- 搜索 STM32Cube
- 比如开发F1，就下载STM32CubeF1

# 新建工程文件夹

文件夹名称
- Drivers
- Middlewares
- Output
- Projects
- User

## Drivers

存放硬件相关的驱动层文件

分为三个子文件夹：
- BSP
- CMSIS
- SYSTEM

### BSP

不一定要有，自己新建。
存放开发板支持包驱动代码，比如外设驱动：I2C，SPI，LCD


### CMSIS

一定会有，去下载的固件包去拷贝。
CMSIS底层代码，启动文件（.s）等。

位置：
C:\Users\195\Desktop\Code\STM32_TEST\en.stm32cubef1-v1-8-5\STM32Cube_FW_F1_V1.8.0\Drivers\CMSIS

但是没有找到任何符合教程说明include文件夹，官方1.8.5和正点原子都没有。



### SYSTEM

一定会有，去正点原子的资料包里拷贝。
存放正点原子系统级核心驱动代码，如syrs.c、delay.c和usart.c等

位置：
D:\书\【正点原子】战舰STM32F103开发板资料 资料盘(A盘)\4，程序源码\1，标准例程-寄存器版本\实验0 新建工程实验\SYSTEM


## Middlewares

存放正点原子提供的中间层组件和第三方中间层文件

## Output

存放工程编译输出文件

## Projects

存放MDK（Keil）工程

新创建一个Keil5工程，MCU选择STM32F103ZE。

## User

存放 main.c 等用户程序


# 添加文件

## Manage Project Items

新建四个分组：
- Startup
- User
- Drivers/System
- Readme

## 添加启动文件
在Startup添加startup_stm32f103xe.s

修改启动文件内容，注释掉SystemInit 三行。
注意这个文件默认只读，需要修改为可写。

```asm

; Reset handler
Reset_Handler   PROC
                EXPORT  Reset_Handler             [WEAK]
                IMPORT  __main
                ;IMPORT  SystemInit
                ;LDR     R0, =SystemInit
                ;BLX     R0               
                LDR     R0, =__main
                BX      R0
                ENDP

```

## 添加SYSTEM源码

添加 
- delay.c 
- sys.c 
- usart.c


# 设置魔术棒

## Target

设置晶振频率：8MHz
设置编译器版本：AC 5


## Output

设置输出文件夹
勾选生成hex

## Listing

同样输出到Output

## C/C++

设置宏定义：STM32F103xE
设置C99模式
设置头文件包含路径，经测试相对路径失效
要把每一个文件夹都包含，比如delay,sys,usart


## Debug

选择STLink

## 结束

创建main.c
编译下载