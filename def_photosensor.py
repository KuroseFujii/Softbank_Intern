#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
import wiringpi
import subprocess
from time import sleep
import signal
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from email.Header import Header 
from email.Utils import formatdate
import smtplib
import os

GPIO.setmode(GPIO.BCM)
sclk = 11
miso = 9
mosi = 10
ce0 = 8
  
GPIO.setup(sclk, GPIO.OUT)
GPIO.setup(miso, GPIO.IN)
GPIO.setup(mosi, GPIO.OUT)
GPIO.setup(ce0, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)


def read(adcnum, sclk, mosi, miso, ce0): #cdsによって光を検出する関数
      
    if adcnum > 7 or adcnum < 0:
        return -1
  
    GPIO.output(ce0, GPIO.HIGH)
    GPIO.output(sclk, GPIO.LOW)
    GPIO.output(ce0, GPIO.LOW)
  
    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
  
    for i in range(5):
        if commandout & 0x80:
            GPIO.output(mosi, GPIO.HIGH)
        else:
            GPIO.output(mosi, GPIO.LOW)
        commandout <<= 1
  
        GPIO.output(sclk, GPIO.HIGH)
        GPIO.output(sclk, GPIO.LOW)
    adcout = 0
  
    for i in range(13):
        GPIO.output(sclk, GPIO.HIGH)
        GPIO.output(sclk, GPIO.LOW)
        adcout <<= 1
        if i>0 and GPIO.input(miso) == GPIO.HIGH:
            adcout |= 0x1
    GPIO.output(ce0, GPIO.HIGH)
    return adcout
