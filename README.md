# Box-drawing Utilities for Labeling Objects Inside your Pictures

Here are some utility python codes that can help you label and manage your images and labels. These codes allow you to surround your object with visualized square lables then convert them to the appropriate form for running yolo. Below are simple descriptions of what each python code does.

## Code Descriptions
### 1. 01_main.py
Executes the labeling program.
> How to use :
1. Requires a "class.txt" file that identifies class names in separate lines.
2. Requires an "Examples/demo/" directory. (Just requires a directory. Doesn't matter the # of images in this directory.)
3. Once the program appears on screen, specify the directory for your images and hit "Load". You will see your very first image file in the center.
4. Next, select object class and hit "Confirm" for the object you want to label. (you don't need to hit "Confirm". it's enough to select an item and focus out the combo_box)
5. Click to label. Only 2 clicks are required for labeling an object. Just to be safe, it is recommended that you click from the upper-left corner to the lower-right corner.(Acutally it dosen't matter.)
6. Delete inserted labels by selecting and hitting "Delete" to delete a selected label, or click "ClearAll" to delete all labels for a single image.
7. Each visualization of label is stored in ".txt" format inside "Labels/{your directory number}/"

> Functions :
1. 'a' : goto next image
2. 'd' : goto prev image
3. 'c' : Copy labels. You can select multiple labels.
4. 'v' : Paste labels.
5. 'r' : remove a last label. If you select a label or labels in label_list_box, the label(s) will be removed.
6. 'z' : remake a last label you made by clicking.
7. 'ctrl + (id)' : If you want to set class without clicking, you can set class with keyboard 'ctrl + (id)'

> these are bugs : 
1. If you focus in this program when you change class with 'ctrl + (id)', your selected class will be changed to selected class in combo_box

### 2. 02_removeEmptyFile.py
Removes redundant images with no label and empty label files.
> How to use :
1. Specify the path to your images and label text files in code. Where to fix is self-evident.

### 3. 03_Labels2Formal.py
Converts labels to appropriate form for feeding yolo network.
> How to use :
1. Specify the path to your label text files and path to save the converted labels.

> Precautions :
1. Must exist "class.txt" file that you modified. When "class.txt" does not exists or is empty file, it asks you'll use default class(=["ParisRedbean","Vita500","TunaCan","VitaJelly","Myzzo","Staples"]).

### 4. 04_trainTestList.py
Creates a list of train set and test set in separate ".list" files. They are named "train.list" and "test.list"
> How to use :
1. Specify the directory where your Label_formal files reside and where your images reside.
2. Specify the percentage to make your test set. (0,100] The remainder will become the train set.

### 5. 05_Formal2Labels.py
In case the original label files are lost, use this code to convert your Label_formal files back to the original label files.
> How to use :
1. Specify path to Label_formal files and the to-be-generated Label files.i
2. Modify class information. Be sure to check item-index correspondence.

### 6. augment.py
Augment your images by adding blur or noise to your images. You can also rotate your image by 180 degrees.
> How to use :
1. Set parameters for augmentation.
2. Run the code.

### 7. make_list_inorder.py
Create a list of all ".jpg" files resident in the current directory. The files are enlisted in order.
> How to use :
1. Modify output list name, most likely "train.list".
2. Run the code.

### 8. make_list_random.py
Create a shuffled list of all ".jpg" files resident in the current directory.
> How to use :
1. Modify output list name, most likely "train.list".
2. Run the code.

### 9. rename.py
Rename files in current directory by replacing a certain expression to another.
> How to use :
1. Modify replace( {src} , {dst} ).
2. Run the code.

### 10. format_list.sh
Shell script to convert newline from DOS format to UNIX format.
> How to use :
1. In UNIX device : type "./format.sh {your file name}" and hit enter.
2. Name says format_"list".sh, but it actually works on all files. Cheers.

### 11. delete_label.py
Delete label files except specific number
> How to use :
1. Set "rest_size" : number of label files which will survive
2. Set "label_path" : set label path 

### 12. missing.py
Print and make a list of imgs/labels whose corresponding label/img is missing. The result will be both printed and made into a list entitled, 'missing.list'. The list is created in the current directory.
> How to use :
1. Run the code.
2. See results from output or 'missing.list'.

### 13. even_out.py
Make a list of data of a specific length. The list contains all of the original data + randomly chosen data out of the original data. The list is created by the "train.list". Unrelevant files that are probably unneeded are enlisted before termination. 
> How to use :
1. Specify goal for list length.
2. Run the code.

### 14. augmnet_multiple.py
Augment a specified percentage of data using multiple augmentation methods. Separate methods are applied to randomly picked data separately to create separate results. They are not applied in combination to a given data.
> How to use :
1. Activate / Deactivate augmentation method.
2. Run the code.

### 15. combine_lists.py
Combine multiple lists into one list, "train.list".
> How to use :
1. Fill in the list of lists to combine.
2. Run the code to create "train.list"

## Notes
1. Strongly advised that Images, Labels, Labels_formal directories be made identically as the provided templates(relative path from source code as well). You can keep things lot simpler this way.
2. Codes without indices (augment, makelist and rename) are meant to be used just before training or testing in darknet. They work for images and corresponding labels residing in the same directory as themselves, so they should be copied to the path to your darknet dataset before use. Be sure that non-relevant .jpg or .txt files are not included in the directory(Otherwise they will be considered a part of your training / test sets).
3. Might have to convert DOS codes to UNIX codes before use. 
