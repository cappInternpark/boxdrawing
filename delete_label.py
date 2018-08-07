import os
from os import walk, getcwd
from PIL import Image
import time
import shutil
import numpy as np


"""-------------------------------------------------------------------""" 

""" Configure """   
rest_size = 5
label_path = "Labels/002/"

""" Get input text file list """
wd = getcwd()
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(label_path):
    txt_name_list.extend(filenames)
    break

label_size = len(txt_name_list)
delete_size = label_size - rest_size
delete_mask = np.random.choice(label_size, delete_size, replace = False)

#print(delete_mask)
#print(txt_name_list)
txt_name_list = np.reshape(txt_name_list, (label_size, 1))
delete_list = txt_name_list[delete_mask]
delete_list = delete_list.ravel()
#print(delete_list)

""" Process """
for delete_txt_name in delete_list:
    delete_txt_path = label_path + delete_txt_name
    os.remove(delete_txt_path)
