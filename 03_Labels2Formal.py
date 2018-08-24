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
import time

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 
classes = []
try:
    with open('class.txt','r') as f:
        lines = f.read().splitlines()
        if len(lines) < 1:
            raise Exception
        for line in lines:
            print("loop")
            classes.append(line)
except Exception as e:
    print("You will use default class?")
    a = input("If you agree, input 'y' :")
    if a is 'y':
        classes = ["ParisRedbean","Vita500","TunaCan","VitaJelly","Myzzo","Staples"]
    else:
        exit()
	
print (classes)
""" Configure Paths"""   
mypath = "Labels/101/"
Imgpath = "Images/101/"
outpath = "Labels_formal/101/"

wd = getcwd()
#list_file = open('%s/001_list.txt'%(wd), 'w')
#not_list_file = open('%s/not_%s_list.txt'%(wd, cls), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)


""" Process """
for txt_name in txt_name_list:
    # txt_file =  open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = mypath + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().splitlines() #for ubuntu, use "\r\n" instead of "\n"
    #print(lines)

    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "w")
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        if(len(line) >= 3):
            ct = ct + 1
            #print(line)		#2\n 615 73 631 83\n 449 205 479 228	
            elems = line.split()
            #print(elems) 		#2 615 73 631 83 449 205 479 228

            cls = elems[0]
            cls_id = classes.index(cls)

            #if(cls_id < 2):	#if(cls_id == 0):
            xmin = elems[1]
            xmax = elems[3]
            ymin = elems[2]
            ymax = elems[4]
            #print(xmin)
            #
            img_path = Imgpath + os.path.splitext(txt_name)[0] + '.jpg'
            print(img_path)
            ##('%s/images/101/%s.JPG'%(wd, os.path.splitext(txt_name)[0]))
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            print(w, h)			# 640 360
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            print(bb)			#0.9 0.2 0.025 0.025
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
#    if(ct != 0):
#        list_file.write('%s/images/001/%s.JPEG\n'%(wd, os.path.splitext(txt_name)[0]))
#    else :
#        not_list_file.write('%s/images/%s/%s.JPEG\n'%(wd, cls, os.path.splitext(txt_name)[0]))
#        not_list_file.write('%s/Labels/%s/%s.txt\n'%(wd, cls, os.path.splitext(txt_name)[0]))
            
                
#list_file.close()       
