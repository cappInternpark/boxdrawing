import os
import shutil
import cv2
from os import walk

x = 6
y = 6
func = 0

sigmaX = 0
sigmaY = 0
"""
print("I was about to explain this .py program, but it's troublesome.")
print("So no explaination")

input_path = raw_input("Enter the input path: ")
output_path = raw_input("Enter the output path: ")
print("0 = blur, 1 = GaussianBlur, 2 = medianBlur.\n(Defalt is 0)")
func = input("Choose the blur type tpye: ")

if len(input_path.strip()) == 0:
	input_path = "./"
if len(output_path.strip()) == 0:
	output_path = "./"
if func > 2 or func < 0 :
	func = 0
print("func Value is {}".format(func))
if func > 0:
	print("kernal size has to be odd.")
	print("median kernal is sqare. so ignore the y value")
x,y = input("Enter the Kernal Size x,y = ")
print("(x,y) = ({},{})".format(x,y))
if func == 1:
	print("Gaussian needs sigma value. (Defalts = 0)")
	sigmaX = input("Value: ")
	print("sigmaX = {}".format(sigmaX))
"""
input_path = "./"
output_path = "./"

#""" img list, label list"""

text_name_list = []
img_name_list = []
for (dirpath, dirnames, f) in walk(input_path):
	for name in f:
		if name.endswith('.txt'):
			text_name_list.append(name)
		elif name.endswith('.png') or name.endswith('.jpg') or name.endswith('.jpeg'):
			img_name_list.append(name)

#f = open(input_path,'r')

list_len = len(img_name_list)

# Specify how much percentage will be blurred and added to the set 
percentage = 0.4

rst_num = int(1/percentage)

cnt = 0
blur_dir_cnt = 6

####Process
for img_name in img_name_list:
        #if(cnt%blur_dir_cnt==0) :
        #       x=3
        #       y=8
        #elif(cnt%blur_dir_cnt==1) :
        #       x=4
        #       y=7
        #elif(cnt%blur_dir_cnt==2) : 
        #       x=5
        #       y=6
        #elif(cnt%blur_dir_cnt==3) : 
        #       x=6
        #       y=5
        #elif(cnt%blur_dir_cnt==4) : 
        #       x=7
        #       y=4
        #elif(cnt%blur_dir_cnt==5) : 
        #       x=8
        #       y=3
        #print(cnt%rst_num)
        
        cnt = cnt + 1
        
        if(cnt%rst_num == 0) :                
        #####Open input img files & copy to dst
                img_path = input_path + img_name
                print("Input: " + img_path)
                print("Name: " + img_name)
                src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                if src is None:
                        print("Wrong file")
                        continue
                print("Success load img")
                dst = src.copy()
            
        ####blur processing
                if func == 0:
                        print("blur function is called")
                        dst = cv2.blur(src,(x,y))
                elif func == 1:
                        print("Gaussian blur function is called")
                        dst = cv2.GaussianBlur(src, (x,y), sigmaX)
                else:
                        print("median blur function is called")
                        # ksize must be odd & >1
                        if (x % 2) == 0:
                                x -= 1
                        dst = cv2.medianBlur(src, x)
                
                # borderType = 	BORDER_REPLICATE	aaaaaa|abcdefgh|hhhhhhh
                #				BORDER_REFLECT:     fedcba|abcdefgh|hgfedcb
                #				BORDER_REFLECT_101: gfedcb|abcdefgh|gfedcba
                #				BORDER_WRAP:        cdefgh|abcdefgh|abcdefg
                # 				BORDER_CONSTANT:	iiiiii|abcdefgh|iiiiiii  with some specified 'i'
            
        #####Save those images
                
                if(func == 0):
                        out_img = output_path + "blur_" + img_name
                        cv2.imwrite(out_img, dst)
                elif(func == 1):
                        out_img = output_path + "gblur_" + img_name
                        cv2.imwrite(out_img, dst)
                else :
                        out_img = output_path + "mblur_" + img_name
                        cv2.imwrite(out_img, dst)

                
                txt_name = text_name_list[img_name_list.index(img_name)]
                if(func == 0):
                        shutil.copyfile(input_path+txt_name, output_path+"blur_"+txt_name)
                elif(func == 1):
                        shutil.copyfile(input_path+txt_name, output_path+"gblur_"+txt_name)
                else :
                        shutil.copyfile(input_path+txt_name, output_path+"mblur_"+txt_name)
        #	txt_path = img_path.replace(".jpg",".txt")
        #	txt_name = img_name.replace(".jpg",".txt")
        #	shutil.copyfile(txt_path,output_path+"blur_"+txt_name)



        #adf	
