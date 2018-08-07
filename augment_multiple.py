# -*- coding: utf-8 -*-
import os
import shutil
import imutils
import random
import cv2
from os import walk
import numpy as np


""""""""""""""" Settings """""""""""""""
"""
Deactivate with 0, Activate with 1
blur: normalized box filter blur
gblur: Gaussian blur
mblur: median blur
gn: Gaussian noise
spn: salt and pepper noise
rot180: rotate 180 degrees (no flipping)
"""
blur=1
gblur=0
mblur=0
gn=1
spn=1
rot180=1

"""
x,y
width and height of blur kernel
"""
x = 6
y = 6

"""
percentage out of all files to augment
"""
percentage = 0.25

"""
sigmaX: standard deviation in x. 0 implies that sigmaX is calculated using kernel size.
sigmaY: standard deviation in y. 0 implies that sigmaY is calculated using kernel size.
"""
sigmaX = 0
sigmaY = 0

""""""""""""""" Settings """""""""""""""

input_path = "./"
output_path = "./"

text_name_list = []
img_name_list = []
for (dirpath, dirnames, f) in walk(input_path):
	for name in f:
		if name.endswith('.txt'):
			text_name_list.append(name)
		elif name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
			img_name_list.append(name)

def add_gaussian_noise(img):
	
	row, col, _ = img.shape
	
	""""""""""""""" Settings """""""""""""""
	"""
	Default values generate data of lightings changed by only a small amount 
	
	Gaussian distribution parameters
	alpha – weight of the first array elements.
	beta – weight of the second array elements.
	gamma – scalar added to each sum.
	"""
	alpha = random.uniform(0.8,1)
	beta = random.uniform(0.8,1)
	gamma = random.uniform(0.8,1)
	strength = 0.001
	""""""""""""""" Settings """""""""""""""
	
	gaussian = np.random.random((row, col, 1)).astype(np.float32)
	gaussian = np.concatenate((gaussian, gaussian, gaussian), axis = 2)
	gaussian_img = cv2.addWeighted(np.asarray(img,np.float32), alpha, strength * gaussian, beta, gamma, dtype=-1)

	return gaussian_img

def add_salt_pepper_noise(X_imgs):
	# Need to produce a copy as to not modify the original image
	X_imgs_copy = X_imgs.copy()
	row, col, _ = X_imgs_copy.shape
	
	""""""""""""""" Settings """""""""""""""
	salt_vs_pepper = 0.2
	amount = 0.004
	""""""""""""""" Settings """""""""""""""
	
	num_salt = np.ceil(amount * X_imgs_copy[0].size * salt_vs_pepper)
	num_pepper = np.ceil(amount * X_imgs_copy[0].size * (1.0 - salt_vs_pepper))
	
	for X_img in X_imgs_copy:
		# Add Salt noise
		coords = [np.random.randint(0, i - 1, int(num_salt)) for i in X_img.shape]
		X_img[coords[0], :] = 1

		# Add Pepper noise
		coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in X_img.shape]
		X_img[coords[0], :] = 0
		
	return X_imgs_copy


list_len = len(img_name_list)
rst_num = int(1/percentage)
cnt = 0

for img_name in img_name_list:
			  
		if(cnt%rst_num == 0) :
				
				img_path = input_path + img_name
#				print("Input: " + img_path)
#				print("Name: " + img_name)
				src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
				if src is None:
#						print("Wrong file")
						continue
#				print("Success load img")
				dst = src.copy()
				txt_name = img_name.split(".")[0]+".txt"

				if blur == 1:
#						print("blur function is called\n")
						dst = cv2.blur(src,(x,y))
						out_img = output_path + "blur_" + img_name
						cv2.imwrite(out_img, dst)
						shutil.copyfile(input_path+txt_name, output_path+"blur_"+txt_name)
						
				if gblur == 1:
						if (x % 2) == 0:
								x = int((x-1)/2)*2+1
						if (y % 2) == 0:
								y = int((y-1)/2)*2+1
#						print("Gaussian blur function is called\n")
						dst = cv2.GaussianBlur(src, (x,y), sigmaX)
						out_img = output_path + "gblur_" + img_name
						cv2.imwrite(out_img, dst)
						shutil.copyfile(input_path+txt_name, output_path+"gblur_"+txt_name)
						
				if mblur == 1:
#						print("median blur function is called\n")
						if (x % 2) == 0:
								x = int((x-1)/2)*2+1
						dst = cv2.medianBlur(src, x)
						out_img = output_path + "mblur_" + img_name
						cv2.imwrite(out_img, dst)
						shutil.copyfile(input_path+txt_name, output_path+"mblur_"+txt_name)
						
				if gn == 1:
#						print("add Guassian noise function is called\n")
						dst = add_gaussian_noise(src)
						out_img = output_path + "gn_" + img_name
						cv2.imwrite(out_img, dst)
						shutil.copyfile(input_path+txt_name, output_path+"gn_"+txt_name)
						
				if spn == 1:
#						print("add salt and pepper noise function is called\n")
						dst = add_salt_pepper_noise(src)
						out_img = output_path + "spn_" + img_name
						cv2.imwrite(out_img, dst)
						shutil.copyfile(input_path+txt_name, output_path+"spn_"+txt_name)

				if rot180 == 1:
#						print("rotate 180 degree function is called\n")
						dst = imutils.rotate_bound(src, 180)
						out_img = output_path + "rot_" + img_name
						cv2.imwrite(out_img, dst)
						text = open(output_path+txt_name, 'r')
						rot_text = open(output_path+"rot_"+txt_name, 'w')

						for line in text.read().split("\n"):
								try:
#										print(line)
										elems = line.split()
										cls_idx = elems[0]
										center_x = float(elems[1])
										center_y = float(elems[2])
										wd = float(elems[3])
										ht = float(elems[4])
										rot_text.write("{0} {1} {2} {3} {4}".format(cls_idx,str(1-center_x),str(1-center_y),str(wd),str(ht)))
										
								except IndexError :
										print("\ndone\n")

						text.close()
						rot_text.close()  
		cnt = cnt + 1
