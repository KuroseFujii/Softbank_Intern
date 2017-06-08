#!/usr/bin/env python
# -*- coding: utf-8 -*-
#パノラマ写真の実装も終了

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
import def_take_pictures as pic
import def_photosensor as photo
import def_mail as mail
import def_panorama as stitch 
pwm_pin_ver= 13   #垂直方向のpwmの出力ピンを指定
pwm_pin_hor= 18  #水平方向のpwmの出力ピンを指定

GPIO.setmode(GPIO.BCM)
sclk = 11
miso = 9
mosi = 10
ce0 = 8
LED_pin = 12
  
GPIO.setup(sclk, GPIO.OUT)
GPIO.setup(miso, GPIO.IN)
GPIO.setup(mosi, GPIO.OUT)
GPIO.setup(ce0, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(LED_pin, GPIO.OUT)    #LED Pin

wiringpi.wiringPiSetupGpio() # GPIO名で番号を指定する
wiringpi.pinMode(pwm_pin_ver, wiringpi.GPIO.PWM_OUTPUT) # 垂直方向のPWM出力を指定
wiringpi.pinMode(pwm_pin_hor, wiringpi.GPIO.PWM_OUTPUT) # 水平方向のPWM出力を指定
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS) # 周波数を固定するための設定
wiringpi.pwmSetClock(375) # 50 Hz。ここには 18750/(周波数) の計算値に近い整数を入れる 375

picnum =1   #保存する写真する名前の数字の初期値
#picmax_hor = (maxhor - minhor)//step_hor  #水平方向の写真を撮影する最大の枚数
#picmax_ver = (maxver - minver)//step_ver  #垂直方向の写真を撮影する最大の枚数
#picmax = (picmax_hor+1)*(picmax_ver + 1 ) #写真を撮影する最大の枚数
picmax = 3

minhor =65  #最小の水平角度
step_hor =10 #水平方向の撮影する間隔
maxhor=minhor +step_hor*picmax#最大の水平角度


minver =88 #最小の垂直角度
maxver=88#最大の垂直角度
step_ver =10  #垂直方向の撮影する間隔

wiringpi.pwmWrite(pwm_pin_ver, minver)#first positon ver
wiringpi.pwmWrite(pwm_pin_hor, minhor)#first positon hor

print('最大で撮影する枚数は%d' % picmax)
js = ['test1.jpg']

from_address ="kurosefujii@gmail.com" #送信メールアドレス
to_address ="rakuten765@gmail.com" #受信メールアドレス


try:
    while True:
        data = photo.read(0, sclk, mosi, miso, ce0) #ドアが開いたことを確認する光データを取得
        print('data = %s'% data)
        if data > 100: 
            while True:
                data2 = photo.read(0, sclk, mosi, miso, ce0) #ドアが開いたことを確認するデータを取得ドアが閉じたことを確認する光データを取得
                print('data2 = %s'% data2)
                sleep(0.2)
                if data2 <1000:
					for duty_ver in range(minver,maxver+step_ver,step_ver):
						wiringpi.pwmWrite(pwm_pin_ver, duty_ver)
						for duty_hor in range(minhor,maxhor,step_hor):
							print('垂直方向%d'% duty_ver)   ,
							print('水平方向%d'% duty_hor)   
							wiringpi.pwmWrite(pwm_pin_hor, duty_hor)
							GPIO.output(LED_pin, GPIO.HIGH)
							countnum =  pic.take_pic(picnum)    #保存する写真する名前の数字を新しくする
							GPIO.output(LED_pin, GPIO.LOW)
							print("'duty")
							js = js + ['test'+str(picnum) + '.jpg']
							sleep(0.2)
							if picnum == picmax:            
								if __name__ == '__main__':
									stitch.panorama()    #パノラマ写真を作成つる関数を呼び出す
									os.chdir("/home/pi/panorama-stitching/fujii_images") #写真が保存されているディレクトリに移動する
									body = u'\n%s\n    --- %s\n' % (u'冷蔵庫の中の写真になります', u'スティーブ・ジョブズ')
									print('mail send!')
									mail.send_email(from_address, to_address, u'今日の名言', body, js)
							picnum = picnum +1
						picnum =1   #次の撮影のための#初期化
						js = ["test1.jpg"] #次の撮影のための#初期化
					break
                else:
                    #GPIO.output(14, GPIO.LOW)
                    print "Refgirator door left open"
                    sleep(0.2) 
        else:
            GPIO.output(14, GPIO.LOW)
            sleep(0.2) 
            
except KeyboardInterrupt:
    pass

wiringpi.pwmWrite(pwm_pin_hor, 0)    #pwm信号を出力しないようにする
wiringpi.pwmWrite(pwm_pin_ver, 0)    #pwm信号を出力しないようにする
GPIO.cleanup()

#実行の仕方 sudo python ./prototype/proto_type4.py
#proto_type3に光検出に以下を加えた
#プログラムが終了したらpwm信号を出力しないようにした  line 211
#水平方向，垂直方向両方動かせるプログラム
#写真を撮影する最大の枚数などを変数として定義 picmax line 21
#変数の名前略語↓
#水平方向　horizon→hor
#垂直方向　vertical→ver
