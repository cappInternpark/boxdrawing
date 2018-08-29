# -*- coding: utf-8 -*-
import os
import shutil
import imutils
import random
import cv2
from skimage import io, transform
from os import walk
import numpy as np
from distutils.dir_util import copy_tree
from pathlib import Path


""""""""""""""" Settings """""""""""""""
"""
Deactivate with 0, Activate with 1
blur: normalized box filter blur
gblur: Gaussian blur
mblur: median blur
gn: Gaussian noise
spn: salt and pepper noise
rot180: rotate 180 degrees (no flipping)
rot90: rotate 90 degrees (counter-clockwise)
"""
blur=0
gblur=0
mblur=0
gn=0
spn=0
rot180=0
rot90=0
rotmul=1

"""
x,y
width and height of blur kernel
"""
x = 5
y = 5

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


class Augment:
    def __init__(self):
        self.rootPath = Path.cwd()
        self.directories = ['augImages', 'sanityCheck', 'data', 'badData', '.',
                            'goodData']
        self.dirDict = {}
        for i in self.directories:
            self.dirDict[i] = self.rootPath / i
        self.ROTATE_MIN = -33.3
        self.ROTATE_MAX = 33.3
        self.ROTATE_PER = 0.15
        
    def getImageFileList(self, path):
        '''RETURNS A LIST OF ALL FILES IN /DATA DIR THAT DO NOT END IN .TXT'''
        imageFileList = os.listdir(self.dirDict[path].as_posix())
        imageFileList = [i for i in imageFileList if i[-3:] != 'txt']
        return imageFileList
    
    def loadImage(self, fileName, path): 
        '''TAKES IN IMAGE FILENAME AND RETURNS IMAGE, OBJECT SIZE (HxW), 
        CLASSES AND LABELS'''
        image = cv2.imread((self.dirDict[path] / fileName).as_posix())
        sizeHW = [image.shape[0], image.shape[1]]
        textFile = fileName.split('.')[0]+'.txt'
        labels = (self.dirDict[path] / textFile).open()
        labels = [i.strip() for i in labels]
        labels = [i.split() for i in labels]
        labels = np.asarray(labels)
        classes = labels[:,0].astype(np.int)
        labels = labels[:,1:].astype(np.float)
        return image, sizeHW, classes, labels
    
    def drawBox(self, img, sizeHW, classes, labels, window):
        '''TAKES IN LABELS IN YOLO FORMAT AND CREATES ANNOTATED IMAGE'''
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(classes)):
            x = (labels[i][0] - labels[i][2]/2) * sizeHW[1]
            y = (labels[i][1] - labels[i][3]/2) * sizeHW[0]
            w = labels[i][2] * sizeHW[1]
            h = labels[i][3] * sizeHW[0]
            cv2.rectangle(img,(int(x),int(y)),(int(x+w),
                           int(y+h)),(0,0,255),2)
            cv2.putText(img,str(int(classes[i])+1),(int(x + w/2),
                            int(y+h/2)), font, 1,(0,0,255),
                            1,cv2.LINE_AA)
        if window:
            cv2.imshow("annotated_img", img)
            key = cv2.waitKey(0)
            return key, img
        else:
            return img
    
    def checkData(self, path):
        '''LOOPS THROUGH DATA IN YOUR DATA FOLDER GIVING A PREVIEW OF LABELED
        IMAGE ALLOWING YOU TO REMOVE IMPROPERLY LABELED IMAGES IF MOVE IS TRUE
        IT WILL MOVE CHECKED DATA INTO SORTED FOLDERS IN ROOT DIRECTORY'''
        print('Press ESC to quit')
        filelist = self.getImageFileList(path)
        move = input('Do you want to seperate sorted data? (Y/N): ').lower()     
        if move == 'y':
            try:
                self.dirDict['goodData'].mkdir()
            except Exception as e:
                print(e.args[0])
            try:
                self.dirDict['badData'].mkdir()
            except Exception as e:
                print(e.args[0])
            print('Press Spacebar to move image into badData dir')
            print('Press any other key to keep data')
        
        for fileName in filelist:
            img, sizeHW, classes, labels, = self.loadImage(fileName, path)
            key,img = self.drawBox(img, sizeHW, classes, labels, window=True)
            image = self.dirDict[path] / fileName
            label = self.dirDict[path] / (fileName.split('.')[0]+'.txt')
            
            if key == 32 and move == 'y':
                print('Removing', fileName)
                image.replace(self.dirDict['badData'] / image.name)
                label.replace(self.dirDict['badData'] / label.name)
            elif key == 27:
                break
            elif move =='y':
                image.replace(self.dirDict['goodData'] / image.name)
                label.replace(self.dirDict['goodData'] / label.name)
        cv2.destroyAllWindows() 
                
    def convert_yolo_2_tf(self,label):
        '''Takes in text file of yolo coords and converts from: 
        [center x, center y, width height] in perentages to:
        [y_min, x_min, y_max, x_max] in percentages'''
        # CREATE NEW BLANK BOX IN FORMAT:   
        # [batch, number of bounding boxes, coords]
        numBoxes = len(label)
        boxes = np.zeros([1,numBoxes,4])
        # FILL IN NEW BOXES
        for i in range(numBoxes):
            boxes[:,i,0] = label[i][1]-label[i][3]/2
            boxes[:,i,1] = label[i][0]-label[i][2]/2
            boxes[:,i,2] = label[i][1]+label[i][3]/2
            boxes[:,i,3] = label[i][0]+label[i][2]/2
        # ENSURE VALUES ARE >= 0
        boxes[boxes<0] = 0
        return boxes
    
    def convert_tf_2_yolo(self, label):
        '''Takes in a list coordinates and converts the array
        [batch, number of bounding boxes, coords] 
        from: [y_min, x_min, y_max, x_max] in % 
        to: [center x, center y, width height] in %'''
        numBoxes = len(label[-1,:,:])
        boxes = np.zeros([numBoxes,4])
        for i in range(numBoxes):
            boxes[i][0] = (label[:,i,1] + label[:,i,3])/2
            boxes[i][1] = (label[:,i,0] + label[:,i,2])/2
            boxes[i][2] = (label[:,i,3] - label[:,i,1])
            boxes[i][3] = (label[:,i,2] - label[:,i,0])
        return boxes
    
    
    def rotateAllPoints(self, angle, tf_labels, sizeHW):
        '''THIS FUNCTION TAKES IN ANGLE, TF B.B LABELS AND THE SIZE OF THE IMAGE 
        AND WILL APPLY ROTATION TO THE LABELS AND RETURN LABELS IN TF FORMAT'''
        n = len(tf_labels[-1,:,:])
        rads = np.deg2rad(angle)
        rotation_matrix = np.array([[np.cos(rads), -np.sin(rads)],
                                    [np.sin(rads), np.cos(rads)]])
        
        # TAKES IN TF FORMAT LABELS AND CREATES POINTS FOR EACH CORNER OF THE
        # BOUNDING BOX IN [X,Y] FORMAT
        boxes = tf_labels[-1,:,:]
        all_points = []
        for i in range(n):
            points=[[boxes[i,1],boxes[i,0]],
                    [boxes[i,1],boxes[i,2]],
                    [boxes[i,3],boxes[i,0]],
                    [boxes[i,3],boxes[i,2]]]
            all_points.append(points)
        
        # CONVERT BOXES FROM IMG ARRAY IN PERCENTAGES FORM TO CARTESIAN PLANE
        all_points = np.asarray(all_points)
        all_points[:,:,1] = -((all_points[:,:,1]*sizeHW[0])-sizeHW[0]/2)
        all_points[:,:,0] = (all_points[:,:,0]*sizeHW[1])-sizeHW[1]/2
        
        # TAKES IN ALL POINTS ROTATES THEM
        rot_points = []
        for i in range(n):
            points = []
            for ii in range(4):
                new_point = np.matmul(rotation_matrix,all_points[i,ii,:])
                points.append(new_point)
            rot_points.append(points)
        rot_points = np.asarray(rot_points)
        
        # CONVERT BACK TO IMG ARRAY FORM IN PERCENTAGES
        rot_points[:,:,1] = (-(rot_points[:,:,1])+sizeHW[0]/2)/sizeHW[0]
        rot_points[:,:,0] = (rot_points[:,:,0]+sizeHW[1]/2)/sizeHW[1]
        
        # CONVERT POINTS TO TF FORMAT
        all_boxes = []
        for i in range(n):
            box = [np.min(rot_points[i,:,1]),np.min(rot_points[i,:,0]),
                   np.max(rot_points[i,:,1]),np.max(rot_points[i,:,0])]
            all_boxes.append(box)
        
        # MAKE SURE ALL VALUES ARE >= 0 AND EXPAND DIMENSION FOR TF FORMAT
        all_boxes = np.asarray(all_boxes)
        all_boxes[all_boxes<0] = 0
        return np.expand_dims(all_boxes,0)
    
    def rotate(self, angle, image, labels, sizeHW):
        '''TAKES IN ANGLE, IMAGE, TF FORMAT LABELS AND IMAGE SIZE AND 
        RETURNS ROTATED IMAGE AND ROTATED LABELS IN YOLO FORMAT'''
        img = transform.rotate(image, angle, mode='edge')
        labels = self.rotateAllPoints(angle, labels, sizeHW)
        labels = self.convert_tf_2_yolo(labels)
        return img, labels
    
    def rotateAugment(self, path):
        files = self.getImageFileList(path)
        try:
            self.ROTATE_MIN = int(input('What min rotation do you want? Default is {}: '.format(self.ROTATE_MIN)))
        except:
            print('Using default value of {}'.format(self.ROTATE_MIN))
        try:
            self.ROTATE_MAX = int(input('What max rotation do you want? Default is {}: '.format(self.ROTATE_MAX)))
        except:
            print('Using default value of {}'.format(self.ROTATE_MAX))
        try:
            self.ROTATE_PER = float(input('What percentage of rotation aug do you want? Default is {}: '.format(self.ROTATE_PER)))
        except:
            print('Using default value of {}'.format(self.ROTATE_PER))
        dataSanity = input('Do you want to sanity check your data? (Y/N) Default is (N): ').lower()
        
        try:
            self.dirDict['augImages'].mkdir()
        except:
            delDir = input('augImages directory allready exists, delete? (Y/N): ').lower()
            if delDir == 'y':
                shutil.rmtree(self.dirDict['augImages'].as_posix())
                self.dirDict['augImages'].mkdir()
               
        if dataSanity == 'y':
            try:
                self.dirDict['sanityCheck'].mkdir()
            except:
                delDir = input('sanityCheck directory allready exists, delete? (Y/N): ').lower()
                if delDir == 'y':
                    shutil.rmtree(self.dirDict['sanityCheck'].as_posix())
                    self.dirDict['sanityCheck'].mkdir()
        
        for file in files:
            image, sizeHW, classes, labels = self.loadImage(file, path)
            labels = self.convert_yolo_2_tf(labels)
            # BOXES WHOSE MIN OR MAX ARE WITHIN 5% OF IMAGE EDGES WONT BE ROTATED
            if len(labels[labels<=0.05]) == 0 and len(labels[labels>=0.95]) == 0:
                if np.random.rand() <= self.ROTATE_PER:
                    angle = np.random.randint(self.ROTATE_MIN, self.ROTATE_MAX)
                    rot_img, rot_coord = self.rotate(angle, image, labels, sizeHW)
                    filename = file.split('.')[0]
                    rot_label = open((self.dirDict['augImages'] / (filename+'_aug.txt'))
                                 .as_posix(),'w')
                    for i in range(len(classes)):
                        rot_label.write('{} {:.7f} {:.7f} {:.7f} {:.7f} \n'
                                    .format(classes[i], 
                                    rot_coord[i][0], rot_coord[i][1], 
                                    rot_coord[i][2], rot_coord[i][3]))
                    rot_label.close()
                    
                    # CONVERT IMAGE TO RGB AND SAVE
                    io.imsave((self.dirDict['augImages'] / (filename+'_aug.jpg'))
                              .as_posix(), rot_img[...,::-1], quality=100)
                    
                    if dataSanity =='y':
                        img = self.drawBox(rot_img, sizeHW, classes, 
                                           rot_coord, window = False)
                        # OPEN CV BUG: BOX AND FONT COLOR VALUES ARE 255
                        img[img>1] = 1
                        io.imsave((self.dirDict['sanityCheck'] / (filename+'_san.jpg'))
                                  .as_posix(), img[...,::-1], quality=100)
                        
    def moveFiles(self, oldPath, newPath):
        copy_tree(self.dirDict[oldPath].as_posix(), 
                  self.dirDict[newPath].as_posix())
        delDir = input('Augmented images copied into data folder, delete augImages path? (Y/N): ').lower()
        if delDir == 'y':
            shutil.rmtree(self.dirDict[oldPath].as_posix())
        
    def makeTrainFile(self, path):
        dataTrainList = open((self.rootPath / 'dataset014_train.txt').as_posix(),'w')
        oldString = "/home/ubuntu/datasets/dataset014/data/"
        files = self.getImageFileList(path)
        for i in files:
            if i[-3::] != 'txt':
                dataTrainList.write(oldString+i+'\n')
        dataTrainList.close()
        print('Created training list for {} files'.format(len(files)))
                        
                        
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
    alpha = random.uniform(0.4,1)
    beta = random.uniform(0.4,1)
    gamma = random.uniform(0.4,1)
    strength = 0.01
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
    salt_vs_pepper = 0.5
    amount = 0.01
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

if rotmul == 1:
                    print("rotation muliple function is called")
                    dh = Augment()
                    dh.rotateAugment(path='.')
                        #out_img = output_path + "rotmul_" + img_name
                        #cv2.imwrite(out_img, dst)
                        #shutil.copyfile(input_path+txt_name, output_path+"rotmul_"+txt_

for img_name in img_name_list:
              
        if(cnt%rst_num == 0) :
                
              img_path = input_path + img_name
#                print("Input: " + img_path)
#                print("Name: " + img_name)
              
              src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
              if src is None:
#                        print("Wrong file")
                         continue
#               print("Success load img")
              dst = src.copy()
              txt_name = img_name.split(".")[0]+".txt"

              if blur == 1:
                        print("blur function is called")
                        dst = cv2.blur(src,(x,y))
                        out_img = output_path + "blur_" + img_name
                        cv2.imwrite(out_img, dst)
                        shutil.copyfile(input_path+txt_name, output_path+"blur_"+txt_name)
                        
              if gblur == 1:
                        if (x % 2) == 0:
                                x = int((x-1)/2)*2+1
                        if (y % 2) == 0:
                                y = int((y-1)/2)*2+1
                        print("Gaussian blur function is called")
                        dst = cv2.GaussianBlur(src, (x,y), sigmaX)
                        out_img = output_path + "gblur_" + img_name
                        cv2.imwrite(out_img, dst)
                        shutil.copyfile(input_path+txt_name, output_path+"gblur_"+txt_name)
                        
              if mblur == 1:
                        print("median blur function is called")
                        if (x % 2) == 0:
                                x = int((x-1)/2)*2+1
                        dst = cv2.medianBlur(src, x)
                        out_img = output_path + "mblur_" + img_name
                        cv2.imwrite(out_img, dst)
                        shutil.copyfile(input_path+txt_name, output_path+"mblur_"+txt_name)
                        
              if gn == 1:
                        print("add Guassian noise function is called")
                        dst = add_gaussian_noise(src)
                        out_img = output_path + "gn_" + img_name
                        cv2.imwrite(out_img, dst)
                        shutil.copyfile(input_path+txt_name, output_path+"gn_"+txt_name)
                        
              if spn == 1:
                        print("add salt and pepper noise function is called")
                        dst = add_salt_pepper_noise(src)
                        out_img = output_path + "spn_" + img_name
                        cv2.imwrite(out_img, dst)
                        shutil.copyfile(input_path+txt_name, output_path+"spn_"+txt_name)
        

              if rot180 == 1:
                        print("rotate 180 degree function is called")
                        dst = imutils.rotate_bound(src, 180)
                        out_img = output_path + "rot_" + img_name
                        cv2.imwrite(out_img, dst)
                        text = open(output_path+txt_name, 'r')
                        rot_text = open(output_path+"rot_"+txt_name, 'w')

                        for line in text.read().split("\n"):
                                try:
#                                        print(line)
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
                        
              if rot90 == 1:
                        text = open(input_path+txt_name, 'r')
                        rot_text = open(output_path+"rot90_"+txt_name, 'w')
                        elems = []
                        moves = []
                        best_move = 0
                        label_num = 0
                        for i, line in enumerate(text.read().split("\n")):
                            try:
                                if(i == 0): 
                                    continue
#                                print(line)
                                tmp = line.split()
                                elems.append([tmp[0], int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4])])
                            except IndexError :
                                print("\ndone\n")
                      
                        for elem in elems:
                            moves.append(140 - elem[1])
                            moves.append(500 - elem[3])
                            
                        moves.append(0)     
                        for move in moves:
                            uncut_num = 0
                            for elem in elems:
                                if(140 <= elem[1] + move < 500 and 140 < elem[3] + move <= 500):
                                    uncut_num = uncut_num + 1
                            if(label_num  <= uncut_num):
                                label_num = uncut_num
                                best_move = move
                    
                        rot_text.write("{0}\n".format(str(label_num)))
                        dst = imutils.translate(src, best_move, 0)
                        dst = imutils.rotate(dst, 90)
                        for idx, elem in enumerate(elems):
                            if(140 <= elem[1] + best_move < 500 and 140 < elem[3] + best_move <= 500):
                                x1 = elem[1] - 320 + best_move
                                y1 = 180 - elem[2]
                                x2 = elem[3] - 320 + best_move
                                y2 = 180 - elem[4]
                                #(x1,y1) -> (y1, -x1)
                                out_x1 = 320 - y2
                                out_y1 = 180 - x1
                                out_x2 = 320 - y1
                                out_y2 = 180 - x2
                                rot_text.write("{0} {1} {2} {3} {4}\n".format(elem[0], str(out_x1), str(out_y1), str(out_x2), str(out_y2)))
                    
                        out_img = output_path + "rot90_" + img_name
                        cv2.imwrite(out_img, dst)
                        text.close()
                        rot_text.close()
        cnt = cnt + 1