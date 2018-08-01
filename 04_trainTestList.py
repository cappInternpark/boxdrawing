import glob, os
from os import getcwd

# Current directory
current_dir = getcwd()
print(current_dir)
images_dir = 'Labels_formal/001'

# Directory where the data will reside, relative to 'darknet.exe'
path_data = 'data/obj/'

# Percentage of images to be used for the test set
percentage_test = 0;

# Create and/or truncate train.txt and test.txt
file_train = open('train.list', 'w')
file_test = open('test.list', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

for pathAndFilename in glob.iglob(os.path.join(current_dir, images_dir, "*.txt")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print(title);
    print(ext);

    if counter == index_test:
        counter = 1
        file_test.write(path_data + title + '.jpg' + "\n")
    else:
        file_train.write(path_data + title + '.jpg' + "\n")
        counter = counter + 1
