# 002 在PIO下开发8051单片机（SDCC）

```c
/*
创建时间   :2022年4月14日
作者        :Vincent
版本        :V1.0


*/
```

[TOC]

# 概述

在VSCODE上用PIO插件对8051进行开发。
由于使用了SDCC编译器，语法上略有不同。并没有完全配置SDCC环境，上传仍然使用STC-ISP。
将会整理一份标准代码留存，如延时，通讯协议等。

# 安装

没有什么特别的，PIO里新建项目，搜“Generic STC89C52RC”。安装速度随缘。
没了。

# Keil和SDCC的区别

## 特殊功能寄存器声明

SDCC不能像Keil一样用sbit和sfr直接再次声明寄存器。

```c
//Keil

sbit LED0 = P1^0;
sfr LED = P1;

//SDCC

#define LED0 P1_0;
#define LED P1;
```

## 延时

不建议用Keil的延时函数，最好使用定时器。
感觉SDCC的靠语句空转延迟的时间比Keil要久。
定时器的基本是精准的，写了一个用定时器0作为ms延迟的函数，后面要改成中断。
正在考虑实现一个millis()的系统时间，以及相关的delay()函数。