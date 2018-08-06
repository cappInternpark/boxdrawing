import os
from os import walk, getcwd
from PIL import Image
import time
import shutil

"""-------------------------------------------------------------------""" 

""" Configure """   
rest_size = 20
label_path = "Labels/001/"

""" Get input text file list """
wd = getcwd()
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(label_path):
    txt_name_list.extend(filenames)
    break

label_size = len(txt_name_list)
delete_size = label_size - rest_size
delete_mask = np.random.choice(label_size, delete_size)
    
delete_list = txt_name_list[delete_mask]

""" Process """
for delete_txt_name in delete_list:
    delete_txt_path = label_path + delete_txt_name
    os.remove(delete_txt_path)
