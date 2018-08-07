from os import getcwd, walk
import random
import os, string, sys

dst_val = 10000

imglist=[]
newlist = open("train.list","w")

for (dirpath,dirname,f) in walk(getcwd()):
	for name in f:
		if name.endswith('.jpg'):
			imglist.append(name)
			newlist.write(name+"\n")
            
size = len(imglist)
to_add = dst_val - size

for cnt in range(0,to_add):
    img = random.choice(imglist)
    newlist.write("{0}\n".format(img))
    imglist.remove(img)

    if not imglist :
        for (dirpath,dirname,f) in walk(getcwd()):
            for name in f:
                if name.endswith('.jpg'):
                    imglist.append(name)
                    
newlist.close()

