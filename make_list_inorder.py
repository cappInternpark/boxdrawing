import glob, os
from os import getcwd

current_dir = getcwd()
file_test = open('train.list', 'w')

for pathAndFilename in glob.glob(os.path.join(current_dir,"*.jpg")):
	print(pathAndFilename)
	file_test.write(pathAndFilename+"\n")
