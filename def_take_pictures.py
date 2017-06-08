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

def take_pic(count): # 写真を撮影する関数
    confirm = "locate /home/pi/panorama-stitching/fujii_images/test1.jpg"   #locateコマンドで保存した写真があるかの確認
    updatedb = "sudo updatedb" #locateコマンドの探す情報を更新する
    delete = "rm /home/pi/panorama-stitching/fujii_images/test1.jpg" #撮影した写真の名前が２回目撮影したときに被らないように削除
    #↑２回目撮影してもまた上書きされるだけだからいらないかも
    #camera = "sudo fswebcam -F 100 --no-timestamp --no-banner /home/pi/panorama-stitching/fujii_images/test1.jpg" # Take a picture
    camera = "sudo fswebcam -F 100 --no-timestamp --no-banner --rotate 90 /home/pi/panorama-stitching/fujii_images/test1.jpg" # Take a picture

    
    led = 12;  #ピン番号
    GPIO.setup(led, GPIO.OUT)
    confirm = confirm.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    delete = delete.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更
    camera = camera.replace('test1','test'+str(count)) #保存する写真する名前の数字を変更

    while True:
        print('check to exist a picture_data')
        ret  =  subprocess.call(confirm,shell = True)
        if ret == 0: #cmdの結果はcatコマンドで画像があれば0を返し、なければ1を返す
            print ret == 0   #File is existed
            print('picture_data is existed.Delete!')
            subprocess.call(delete,shell = True) #file delete
            break
        else:
            #print "non file" #File is not existed
            break
    while True:
        print('Take a picture')
        GPIO.output(led, GPIO.HIGH)
        subprocess.call(camera,shell = True)
        subprocess.call(updatedb,shell = True)
        GPIO.output(led, GPIO.LOW)
        print('check to exist a picture_data_2nd')
        ret  =  subprocess.call(confirm,shell = True)

        if ret == 0: #cmdの結果はcatコマンドで画像があれば0を返し、なければ1を返す
            print ret == 0   #File is existed
            print('picture_data is existed.Upload!')
        else:
            print "we can't take a picture" #File is not existed
            print('one more take a picture')
            print('Waitig for 10 sec ')
            #GPIO.output(4, GPIO.HIGH)
            #time.sleep(10)
            #GPIO.output(4, GPIO.LOW)
            time.sleep(10)
            continue
        break
    return count
