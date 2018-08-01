# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

import os
from os import walk, getcwd
from PIL import Image

def restore_label(label_orig_path, label_orig, save_path):
    orig_file = open(label_orig_path+label_orig, "r")
    wr_file = open(save_path+label_orig,"w")
    
    for lines in orig_file.read().splitlines():
        print(lines)
        # class name / center coord x,y / width, height
        elems = lines.split()
        cls_idx = elems[0]
        # normalized by size of image coordinates
        center_x = float(elems[1])
        center_y = float(elems[2])
        wd = float(elems[3])
        ht = float(elems[4])
        
        wr_file.write("1\n{0} {1} {2} {3} {4}".format(class_name, str(int(img_wd*(center_x-0.5*wd))), str(int(img_ht*(center_y-0.5*ht))), str(int(img_wd*(center_x+0.5*wd))), str(int(img_ht*(center_y+0.5*ht)))))
        
    wr_file.close()
    
    
    
""""""""" Modify before use """""""""""
# Set basic information of image and class
class_name = "Staples"

# Image width and height
img_wd = 640
img_ht = 360
                            
# Set directory of image files
label_formal_path = "Labels_formal/001/"
label_save_path = "Labels/001/"
""""""""" Modify before use """""""""""


classes = ["001"]
cls = "001"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
    
""" Get input label file list """
label_name_list = []
for (dirpath, dirnames, filenames) in walk(label_formal_path):
    label_name_list.extend(filenames)
    break

""" Restore original label from formalized label """
for label_formal_file in label_name_list :
    restore_label(label_formal_path, label_formal_file, label_save_path)