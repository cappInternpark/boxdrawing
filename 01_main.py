#-------------------------------------------------------------------------------
# Name:        Object bounding box label tool
# Purpose:     Label object bboxes for ImageNet Detection data
# Author:      Qiushi
# Created:     06/06/2014

#
#-------------------------------------------------------------------------------

# Undo, Class Leaderborad, Same Class Color, Auto Class Comfirm, Right Click Delete
from __future__ import division
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import os
import glob
import random

# colors for the bboxes
# https://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
# above link is color dictionary in matlib
COLORS = ['red', 'blue', 'olive', 'teal', 'skyblue', 'orange',\
          'cyan', 'green', 'yellow', 'magenta', 'black']
# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("LabelTool!")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.currentLabelclass = ''
        self.cla_can_temp = []
        self.classcandidate_filename = 'class.txt'

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None
        self.bboxcopyList = []
        self.bboxSel = None

        # -----------------   stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2,sticky = W+E)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("s", self.cancelBBox)
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.parent.bind("c", self.copyLabel) # press 'c' to copy label
        self.parent.bind("v", self.pasteLabel) # press 'v' to paste label
        self.parent.bind("r", self.deleteLabel) # press 'r' to delete label
        self.parent.bind("z", self.undoLabel) # press 'z' to undo label
        self.mainPanel.grid(row = 1, column = 1, rowspan = 4, sticky = W+N)

        # choose class
        self.classname = StringVar()
        self.classcandidate = ttk.Combobox(self.frame,state='readonly',textvariable=self.classname)
        self.classcandidate.grid(row=1,column=2)
        if os.path.exists(self.classcandidate_filename):
        	with open(self.classcandidate_filename) as cf:
        		for line in cf.readlines():
        			# print line
        			self.cla_can_temp.append(line.strip('\n'))
        #print self.cla_can_temp
        self.classcandidate['values'] = self.cla_can_temp
        self.classcandidate.current(0)
        self.currentLabelclass = self.classcandidate.get() #init
        self.btnclass = Button(self.frame, text = 'ComfirmClass', command = self.setClass)
        self.btnclass.grid(row=2,column=2,sticky = W+E)
        self.classcandidate.bind("<FocusIn>", self.setClass) # 
		# Showing Class LeaderBoard

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 3, column = 2,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 22, height = 12)
        self.listbox.config(selectmode=EXTENDED)
        self.listbox.grid(row = 4, column = 2, sticky = N+S)
        self.btnDel = Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 5, column = 2, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 6, column = 2, sticky = W+E+N)
        self.listbox.bind("<Button-3>", self.delBBox)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 7, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)


        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Examples:")
        self.tmpLabel2.pack(side = TOP, pady = 5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side = TOP)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        # for debugging
##        self.setImage()
##        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            s = self.entry.get()
            self.parent.focus()
            self.category = int(s)
        else:
            s = r'D:\workspace\python\labelGUI'
##        if not os.path.isdir(s):
##            tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
##            return
        # get image list
        self.imageDir = os.path.join(r'./Images', '%03d' %(self.category))
        #print self.imageDir 
        #print self.category
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        #print self.imageList
        if len(self.imageList) == 0:
            print ('No .JPG images found in the specified dir!')
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        self.outDir = os.path.join(r'./Labels', '%03d' %(self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)

        # load example bboxes
        #self.egDir = os.path.join(r'./Examples', '%03d' %(self.category))
        self.egDir = os.path.join(r'./Examples/demo')
        print (os.path.exists(self.egDir))
        if not os.path.exists(self.egDir):
            return
        filelist = glob.glob(os.path.join(self.egDir, '*.jpg'))
        self.tmp = []
        self.egList = []
        random.shuffle(filelist)
        for (i, f) in enumerate(filelist):
            if i == 3:
                break
            im = Image.open(f)
            r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
            new_size = int(r * im.size[0]), int(r * im.size[1])
            self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
            self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
            self.egLabels[i].config(image = self.egList[-1], width = SIZE[0], height = SIZE[1])

        self.loadImage()
        print ('%d images loaded from %s' %(self.total, s))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.img.save(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int(line.strip())
                        continue
                    # tmp = [int(t.strip()) for t in line.split()]
                    tmp = tuple(line.split())
                    #print tmp
                    #
                    idx =  self.sortLabelIdx(tmp, self.cla_can_temp)
                    try:
                        class_idx = self.cla_can_temp.index(tmp[0])
                    except ValueError:
                        class_idx = len(self.cla_can_temp)+len(self.bboxList)
                    self.bboxList.insert(idx, tmp)
                    tmpId = self.mainPanel.create_rectangle(int(tmp[1]), int(tmp[2]), \
                                                            int(tmp[3]), int(tmp[4]), \
                                                            width = 2, \
                                                            outline = COLORS[class_idx % len(COLORS)])
                    # print tmpId
                    self.bboxIdList.insert(idx, tmpId)
                    self.listbox.insert(idx, '%s : (%d, %d) -> (%d, %d)' %(tmp[0],int(tmp[1]), int(tmp[2]), \
                    												  int(tmp[3]), int(tmp[4])))
                    self.listbox.itemconfig(idx, fg = COLORS[class_idx % len(COLORS)])

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' %len(self.bboxList))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print ('Image No. %d saved' %(self.cur))

    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            #self.bboxList.append((x1, y1, x2, y2, self.currentLabelclass))
			#########################
            tmp = (self.currentLabelclass, str(x1), str(y1), str(x2), str(y2))
            idx =  self.sortLabelIdx(tmp, self.cla_can_temp)
            try:
                class_idx = self.cla_can_temp.index(tmp[0])
            except ValueError:
                class_idx = len(self.cla_can_temp)+len(self.bboxList)
            #########################
            self.bboxList.insert(idx, tmp)
            self.bboxIdList.insert(idx, self.bboxId)
            self.bboxId = None
            self.listbox.insert(idx, '%s : (%d, %d) -> (%d, %d)' %(self.currentLabelclass,x1, y1, x2, y2))
            self.listbox.itemconfig(idx, fg = COLORS[class_idx % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width = 2, \
                                                            outline = COLORS[self.cla_can_temp.index(self.currentLabelclass) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self, event = None):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            if event is None:
                return
            if int(event.y/22) < self.listbox.size():
                idx = self.listbox.index("@{},{}".format(event.x, event.y))
            else:
                return
        else:
            idx = int(sel[0])
        
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def setClass(self, event = None):
        if event is None:
            self.currentLabelclass = self.classcandidate.get()
            print ('set label class to :',self.currentLabelclass)
        else:
            if self.currentLabelclass != self.classcandidate.get():
                self.currentLabelclass = self.classcandidate.get()
                print ('set label class to :',self.currentLabelclass)
		
    def copyLabel(self,event = None):
        if len(self.bboxList) is 0:
                return
        sel = self.listbox.curselection()
        self.bboxcopyList = []
        if len(sel) is 0:
            self.bboxcopyList.append(self.bboxList[len(self.bboxList) - 1])
        else:
            for idx in sel:
                self.bboxcopyList.append(self.bboxList[idx])

    def pasteLabel(self, event = None):
        if(len(self.bboxcopyList) is 0):
            return
        for bboxcopy in self.bboxcopyList:
            bboxcopyId = self.mainPanel.create_rectangle(bboxcopy[1], bboxcopy[2],\
                                                        bboxcopy[3], bboxcopy[4],\
                                                        width = 2,\
                                                        outline = (COLORS[len(self.bboxList)% len(COLORS)]))
            self.bboxList.append(bboxcopy)
            self.bboxIdList.append(bboxcopyId)
            self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' %(bboxcopy[0],\
                                        int(bboxcopy[1]), int(bboxcopy[2]),\
                                        int(bboxcopy[3]), int(bboxcopy[4])))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    def deleteLabel(self, event = None):
        if len(self.bboxList) is 0:
                return
        sel = self.listbox.curselection()
        if len(sel) is 0:
            self.mainPanel.delete(self.bboxIdList[len(self.bboxIdList)-1])
            self.listbox.delete(len(self.bboxIdList)-1)
            self.bboxIdList.pop()
            self.bboxList.pop()
        else:
            for idx in reversed(list(sel)):
                self.mainPanel.delete(self.bboxIdList[idx])
                self.bboxIdList.pop(idx)
                self.bboxList.pop(idx)
                self.listbox.delete(idx)
		    
    def undoLabel(self, event = None):
        print(self.bboxList)
        print(self.bboxIdList)
        return
	
    def sortLabelIdx(self, label, classes):
        if type(label) is tuple:
            key = label[0]
        elif type(label) is list:
            return len(self.bboxList)
        elif type(label) is str:
            key = label
        idx = 0
        try:
            classes.index(key)
        except ValueError:
            print("Warning: doesn't exist {} class".format(key))
            return len(self.bboxList)
        try:
            # Linear Search
            for bbox in self.bboxList:
                if classes.index(bbox[0]) > classes.index(key):
                    break;
                idx = idx + 1
        except ValueError:
            return idx
        return idx

##    def setImage(self, imagepath = r'test2.png'):
##        self.img = Image.open(imagepath)
##        self.tkimg = ImageTk.PhotoImage(self.img)
##        self.mainPanel.config(width = self.tkimg.width())
##        self.mainPanel.config(height = self.tkimg.height())
##        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
