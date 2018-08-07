from os import getcwd, walk

txtlist=[]
imglist=[]
elselist=[]

for (dirpath,dirname,f) in walk(getcwd()):
	for name in f:
		if name.endswith('.txt'):
			txtlist.append(name)
		elif name.endswith('.jpg'):
			imglist.append(name)
		else:
			elselist.append(name)

missingimg=[]
missinglabel=[]
cntimg=0
cntlabel=0
print('list of txt/img with missing pair')

for img in imglist:
	if img.split(".")[0]+".txt" not in txtlist:
		missinglabel.append(img)
		cntlabel += 1

for txt in txtlist:
	if txt.split(".")[0]+".jpg" not in imglist:
		missinglimg.append(txt)
		cntlabel += 1

missingimg.sort()
missinglabel.sort()

missing = open("missing.list",'w')

print "missing img: {0}".format(cntimg)
missing.write('missing img: {0}'.format(cntimg))

for name in missingimg:
	print name
	missing.write(name)

print "missing label: {0}".format(cntlabel)
missing.write('missing label: {0}'.format(cntlabel))

for name in missinglabel:
	print name
	missing.write(name)

missing.close()

print("Unrelevant files detected:")
for name in elselist:
	print name
