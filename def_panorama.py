#!/usr/bin/env python
# -*- coding: utf-8 -*-
# USAGE
# python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 
#sudo python ./panorama-stitching/stitch.py --first ./images/bryce_left_01.png --second ./images/bryce_right_01.png
# import the necessary packages
#3毎に対応


from pyimagesearch.panorama import Stitcher
import argparse
import imutils
import cv2
import os
def panorama():  #メールを送信する関数
	os.chdir("/home/pi/panorama-stitching/fujii_images") #画像があるディレクトリに移動する

	imageA = cv2.imread("test2.jpg")
	imageB = cv2.imread("test1.jpg")
	angle =270  #回転する角度（反時計回り）

	stitcher = Stitcher()
	(preresult, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

	vis = cv2.flip(vis,1)
	#cv2.imshow("Keypoint Matches1", vis)
	#cv2.imshow("preResult", preresult)
	cv2.imwrite("pre_result.jpg", preresult)

	imageC = cv2.imread("pre_result.jpg")
	imageD = cv2.imread("test3.jpg")
	imageC = cv2.flip(imageC,1)
	imageD = cv2.flip(imageD,1)

	(result, vis2) = stitcher.stitch([imageC, imageD], showMatches=True)
	#cv2.imshow("Keypoint Matches2", vis2)

	result = cv2.flip(result,1)
	#cv2.imshow("Result", result)
	cv2.imwrite("result.jpg", result)
	cv2.waitKey(0)
