# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO 
@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
from os import walk, getcwd
from PIL import Image

""" Configure Paths"""
mypath = "Labels/001/"

classes=["001"]
cls = "001"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    """ Open input text files """
    txt_path = mypath + txt_name
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\r\n')   #for ubuntu, use "\r\n" instead of "\n"
    # print(lines)

    """ Convert the data to YOLO format """
    isEmpty = 0
    for line in lines:
        print(line)
        print(len(line))
        if (len(line) <= 2):
            isEmpty = 1
            break
        else :
            break

    txt_file.close()

    if(isEmpty == 1) :
        os.remove('%s/images/%s/%s.jpg' % (wd, cls, os.path.splitext(txt_name)[0]))
        os.remove('%s/Labels/%s/%s.txt' % (wd, cls, os.path.splitext(txt_name)[0]))



