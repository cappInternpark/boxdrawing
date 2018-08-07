from os import getcwd, walk
import random
import os, string, sys

dst_val = 17000

imglist=[]
newlist = open("l0.list","w")

for (dirpath,dirname,f) in walk(getcwd()):
	for name in f:
		if name.endswith('.jpg'):
			imglist.append(name)
			newlist.write("{0}/{1}\n".format(getcwd(),name))			

print("Wrote {0} images".format(len(imglist)))

size = len(imglist)
to_add = dst_val - size

for cnt in range(0,to_add):
	img = random.choice(imglist)
	newlist.write("{0}/{1}\n".format(getcwd(),img))
	imglist.remove(img)
	
	print(len(imglist))

	if len(imglist) == 0 :
		print("RELOAD")
		for (dirpath,dirname,f) in walk(getcwd()):
			for name in f:
				if name.endswith('.jpg'):
					imglist.append(name)
					
newlist.close()

