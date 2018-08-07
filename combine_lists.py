# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

import os
import glob
from os import getcwd
from PIL import Image
    
def restore_label(src, save_path):
	orig_file1 = open(src, "r")
#	orig_file2 = open(dest, "r")
	wr_file = open(save_path,"a")
	
	lines_1 = orig_file1.read().splitlines()
#	lines_2 = orig_file2.read().splitlines()
#	num = lines_1[0] + lines_2[0]
	
#del lines_1[0]
#del lines_2[0]
	
#wr_file.write("{}\n".format(num))
	for lines in lines_1:
		wr_file.write("{}\n".format(lines))

#	for lines in lines_2:
#		wr_file.write("{}\n".format(lines))
	
	orig_file1.close()
#	orig_file2.close()
	wr_file.close()
	
	
""""""""" Modify before use """""""""""
paths = ["l0.list","l1.list","l2.list","l3.list","l4.list","l5.list"]
#              base             added~~~

label_save_path = "Labels/111/"
""""""""" Modify before use """""""""""

wd = getcwd()
    
""" Get input label file list """
label_name_list = []
#for filename in glob.iglob(os.path.join(pathes[0], "*.txt")):
#	label_name_list.append(os.path.basename(filename))

for label in paths:
	restore_label(label, "train.list")
	
	
	
	
