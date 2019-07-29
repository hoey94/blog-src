---
title: HDMI连接Raspberry
date: 2019-07-29 22:26:00
categories: 物联网
---

通常情况下，树莓派会自动检测显示器的类型并修改配置。但有时，自动检测的结果可能不正确。如果你的树莓派连接到电视上但没有任何显示的话，你要考虑手动修改树莓派的显示配置了

![https://i.loli.net/2019/07/30/5d3f1b5a7dc4c45534.jpeg](https://i.loli.net/2019/07/30/5d3f1b5a7dc4c45534.jpeg)

下面我们手动修改/boot/config.txt文件。记得修改前备份一个，以下是参数文件：

```shell
# For more options and information see
# http://rpf.io/configtxt
# Some settings may impact device functionality. See link above for details

# uncomment if you get no picture on HDMI for a default "safe" mode
#hdmi_safe=1

# uncomment this if your display has a black border of unused pixels visible
# and your display can output without overscan
disable_overscan=1

# uncomment the following to adjust overscan. Use positive numbers if console
# goes off screen, and negative if there is too much border
#overscan_left=16
#overscan_right=16
#overscan_top=16
#overscan_bottom=16

# uncomment to force a console size. By default it will be display's size minus
# overscan.
#framebuffer_width=1280
#framebuffer_height=720

# uncomment if hdmi display is not detected and composite is being output
hdmi_force_hotplug=1

# uncomment to force a specific HDMI mode (this will force VGA)
hdmi_group=1
hdmi_mode=4

# uncomment to force a HDMI mode rather than DVI. This can make audio work in
# DMT (computer monitor) modes
hdmi_drive=2

# uncomment to increase signal to HDMI, if you have interference, blanking, or
# no display
config_hdmi_boost=4

# uncomment for composite PAL
#sdtv_mode=2

#uncomment to overclock the arm. 700 MHz is the default.
#arm_freq=800

# Uncomment some or all of these to enable the optional hardware interfaces
#dtparam=i2c_arm=on
#dtparam=i2s=on
#dtparam=spi=on

# Uncomment this to enable the lirc-rpi module
#dtoverlay=lirc-rpi

# Additional overlays and parameters are documented /boot/overlays/README

# Enable audio (loads snd_bcm2835)
dtparam=audio=on
start_x=1
gpu_mem=128
enable_uart=1

#disable_camera_led=1
hdmi_ignore_edid=0xa5000080
```

看这个[https://wenku.baidu.com/view/a8a1554e71fe910ef02df893.html](https://wenku.baidu.com/view/a8a1554e71fe910ef02df893.html)，学一下各个参数详解

学完之后了解一下怎么调hdmi_mode这个参数[https://zhidao.baidu.com/question/519865882625562245.html](https://zhidao.baidu.com/question/519865882625562245.html)
