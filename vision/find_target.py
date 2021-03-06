import cv2
import os
import numpy as np
import manipulate_image as MI
import validate_target as VT
from util.stopwatch import stopwatch as SW
import image_calculations as IC
from datetime import datetime


def find_valids(img_orig, calibration, desired_cnt):
    """[summary]

    Arguments:
        img_orig {[type]} -- [description]
        calibration {[type]} -- [description]
        desired_cnt {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    path = "/" + "/".join(os.getcwd().split("/")[1:3]) + "/test_images/"
    print("path: " + path)
    debug = calibration['debug']
    search = calibration['search']
    angle = 1000
    valid_update = False
    img_copy = np.copy(img_orig)
    lower_bound = np.array(calibration["green"]["green_lower"])
    upper_bound = np.array(calibration["green"]["green_upper"])
    if debug:
        timer_ft = SW('ft')
        timer_ft.start()
    hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    if debug:
        elapsed = timer_ft.get()
        print("DEBUG: cvt took " + str(elapsed))
    if debug:
        timer_ft.start()
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    if debug:
        elapsed = timer_ft.get()
        print("DEBUG: inrange took " + str(elapsed))
    if debug:
        timer_ft.start()
    erode_and_diliate = MI.erodeAndDilate(mask)
    if debug:
        elapsed = timer_ft.get()
        print("DEBUG: erode_and_dilate took " + str(elapsed))
    if debug:
        timer_ft.start()
    ret, mask_thresh = cv2.threshold(
        erode_and_diliate, 127, 255, cv2.THRESH_BINARY)
    if debug:
        elapsed = timer_ft.get()
        print("DEBUG: threshold took " + str(elapsed))
    if debug:
        time = datetime.now().strftime("%s")
        cv2.imwrite(path +
                    time+"_image_orig.png", img_orig)
        cv2.imwrite(path+time+"_mask.png", mask)
        cv2.imwrite(path+time+"_mask.png", mask_thresh)
        cv2.imwrite(path+time +
                    "_erode_and_diliate.png", erode_and_diliate)
    if search:
        valid, cnt = VT.find_valid_target(mask_thresh, desired_cnt)
        if valid:
            valid_update = True
            hull = cv2.convexHull(cnt[0])
            cx, cy = IC.findCenter(hull)
            if debug:
                line_img = MI.drawLine2Target(mask_thresh, cx, cy)
                cv2.imwrite(path +
                            time + "target_lined.png", line_img)
            angle = IC.findAngle(img_orig, cx)
    return angle, valid_update
