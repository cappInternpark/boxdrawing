# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

import os
import glob
from os import getcwd
from PIL import Image

def restore_label(label_orig_path, label_orig, save_path):
    orig_file = open(label_orig_path+label_orig, "r")
    wr_file = open(save_path+label_orig,"w")
    lines_list = orig_file.read().splitlines()
    wr_file.write("{}".format(len(lines_list)))
    for lines in lines_list:
        wr_file.write("\n")
        # class name / center coord x,y / width, height
        elems = lines.split()
        cls_idx = int(elems[0])
        # normalized by size of image coordinates
        center_x = float(elems[1])
        center_y = float(elems[2])
        wd = float(elems[3])
        ht = float(elems[4])
        wr_file.write("{0} {1} {2} {3} {4}".format(classes[cls_idx], str(int(img_wd*(center_x-0.5*wd))), str(int(img_ht*(center_y-0.5*ht))), str(int(img_wd*(center_x+0.5*wd))), str(int(img_ht*(center_y+0.5*ht)))))
        #wr_file.write("{0}\n{1} {2} {3} {4} {5}".format(num, classes[cls_idx], str(int(img_wd*(center_x-0.5*wd))), str(int(img_ht*(center_y-0.5*ht))), str(int(img_wd*(center_x+0.5*wd))), str(int(img_ht*(center_y+0.5*ht)))))
        
    wr_file.close()
    
    
    
""""""""" Modify before use """""""""""
# Set basic information of image and class
classes = ["ParisRedbean","Vita500","TunaCan","VitaJelly","Myzzo","Staples"]

# Image width and height
img_wd = 640
img_ht = 360
                            
# Set directory of image files
label_formal_path = "Labels_formal/001/"
label_save_path = "Labels/001/"
""""""""" Modify before use """""""""""

wd = getcwd()
    
""" Get input label file list """
label_name_list = []
for filename in glob.iglob(os.path.join(label_formal_path, "*.txt")):
    label_name_list.append(os.path.basename(filename))

""" Restore original label from formalized label """
for label_formal_file in label_name_list :
    print(label_formal_file)
    restore_label(label_formal_path, label_formal_file, label_save_path)