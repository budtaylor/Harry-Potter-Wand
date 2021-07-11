# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 22:51:23 2020

@author: John
"""

import sys
import os
import time
sys.path.append('/home/pi/.local/lib/python3.7/site-packages/cv2/')
import cv2
import numpy as np
import RPi.GPIO as GPIO

from picamera.array import PiRGBArray
from picamera import PiCamera

import dependencies.image_processing as imp
#import dependencies.spells as spells
ledPin = 11    # RPI Board pin11

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
    GPIO.output(ledPin, GPIO.LOW) # Set ledPin low to off led
    GPIO.setwarnings(False)

def main():

    label_encode = ['Incendio','Reparo','Wingardium']

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(1.0)

    #%% Create Blob Detector 
    detector = imp.create_blob_detector()

    # Create new SVM and load model
    filepath = os.path.dirname(os.path.abspath(__file__))
    filename = filepath + '//' + "dependencies" + "//" + "svm_model_data_gen_rbpi.yml"
    svm = cv2.ml.SVM_load(filename)

    # Make hog transformer for SVM
    hog = imp.make_hog()

    ## List to hold coordinates of detected blobs and hold list of blob points
    blob_points = []

    # Frame Size
    w_frame = 480;
    h_frame = 640;

    count = 0
    trace_len = 25
    trace_time = 0
    timeout = 5
    duration = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    label = 'blank'

    # Create Blank Frame to Overlay key points
    blank_image = np.zeros((w_frame,h_frame),dtype = np.uint8)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture,\
                                           format="bgr", use_video_port=True):
        # timer for blob velocity detection
        start = time.time()
        
        # grab the raw NumPy array representing the image
        frame = frame.array
          
        # Turn to gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        # Uncomment for Debugging
#         cv2.putText(frame, label, (50,50), font, 1,\
#                         (0, 255, 255), 2, cv2.LINE_4)
        
        # Detecting keypoints on video stream
        keypoints = detector.detect(frame)
        
        # Uncomment for Debugging
#         #Uncomment to see video stream
#         frame_with_keypoints = cv2.drawKeypoints(frame,\
#                                                  keypoints, np.array([]),\
#                                                  (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Get coordinates of blob
        blob_cords = cv2.KeyPoint_convert(keypoints)
        
        # Initialize Points array
        if len(blob_cords) != 0:
            if count == 0:
                blob_points.append(blob_cords[0])
                count += 1
            elif count > 0:
                imp.check_speed(blob_points[count-1],blob_cords[0],duration)
                blob_points.append(blob_cords[0])
                count += 1
                # timer for blob velocity detection
                stop = time.time()
                duration = stop-start
            else:
                # timer for blob velocity detection
                stop = time.time()
                duration = stop-start
                continue
        else:
            # timer for blob velocity detection
            stop = time.time()
            duration = stop-start
            
        for i in range(1,len(blob_points)):
            cv2.line(blank_image, tuple(blob_points[i-1]),\
                     tuple(blob_points[i]), (255, 255, 255), 3)
            # Uncomment for Debugging
#             cv2.line(frame_with_keypoints, tuple(blob_points[i-1]),\
#                      tuple(blob_points[i]), (255, 0, 0), 3)    # show image for drawing trace
        # Uncomment for Debugging   
#         cv2.imshow("frame",frame_with_keypoints)
            
        # Truncate wand trace length and process in SVM model
        if count > trace_len:
            # Start new trace 
            blob_points = []
            
            # Prep Image for SVM
            img_resized = imp.bbox_and_resize(blank_image)
            img_hog = hog.compute(img_resized)
            
            prediction = svm.predict(img_hog.T, True)
            label = label_encode[int(prediction[1])]
            print(label)
            
            if label == 'Wingardium':
#                 spells.luomos_max(pixels)
                #GPIO.cleanup()
                #GPIO.output(ledPin, GPIO.LOW)
                #GPIO.cleanup()
                print("Wingardium Dude")
 #               GPIO.cleanup()
            elif label == 'Incendio':
                print("TRIANGLE")
                GPIO.output(ledPin, GPIO.HIGH)
                time.sleep(8)
                GPIO.output(ledPin, GPIO.LOW)
                #time.sleep(0.3)
                #GPIO.output(ledPin, GPIO.HIGH)
                #time.sleep(.5)
                #GPIO.output(ledPin, GPIO.LOW)
                #time.sleep(0.5)
                #GPIO.output(ledPin, GPIO.HIGH)
                #time.sleep(.2)
                #GPIO.output(ledPin, GPIO.LOW)
#                time.sleep(1)
 #               print("TRIANGLE")
                #GPIO.cleanup()
            elif label == 'Circle' or label == 'Square':
#                spells.leviosa()
                #GPIO.cleanup()
                #GPIO.output(ledPin, GPIO.LOW)
                #GPIO.cleanup()
                print("CIRCLE")
                
            # Reset Blank Frame
            blank_image = np.zeros((w_frame,h_frame), dtype = np.uint8)
            
            count = 0    
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        
        stop_timeout = time.time()
        trace_time += start - stop_timeout
        
        if trace_time > timeout:
            # Start new trace 
            blob_points = []
            trace_time = 0
            
            # Reset Blank Frame
            blank_image = np.zeros((w_frame,h_frame), dtype = np.uint8)
            
            # Uncomment for Debugging
#             for i in range(1,len(blob_points)):
#                 cv2.line(frame_with_keypoints, tuple(blob_points[i-1]),\
#                      tuple(blob_points[i]), (255, 0, 0), 3)
        
        if key == ord("q"):
            break

if __name__ == "__main__":
    setup()
    main()

