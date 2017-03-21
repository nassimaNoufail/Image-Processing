from Tkinter import *
from ttk import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import tkMessageBox
import cv2
import math
import random
import numpy as np

class Main(Frame):
    img = None
    originImg = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.readImage)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        editmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Add pepper and salt noise", command=lambda: self.addNoise(0))
        editmenu.add_command(label="Add pepper noise", command=lambda: self.addNoise(1))
        editmenu.add_command(label="Add salt noise", command=lambda: self.addNoise(2))
        editmenu.add_command(label="Reset", command=self.reset)

        toolmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tool", menu=toolmenu)
        toolmenu.add_command(label="Neighbor Averaging(3x3)"
                             , command=lambda: self.smoothing(img, 'neighborhood_averaging', 1))
        toolmenu.add_command(label="Neighbor Averaging(5x5)"
                             , command=lambda: self.smoothing(img, 'neighborhood_averaging', 2))
        toolmenu.add_command(label="median filter(3x3)", command=lambda: self.smoothing(img, 'median_filtering', 1))
        toolmenu.add_command(label="median filter(5x5)", command=lambda: self.smoothing(img, 'median_filtering', 2))
        toolmenu.add_command(label="Bilateral filter(3x3, sigma_c=50, sigma_s=3)"
                             , command=lambda: self.smoothing(img, 'Bilateral_filter', 1))
        toolmenu.add_command(label="Min filtering(3x3)"
                             , command=lambda: self.smoothing(img, 'Min_filtering', 1))
        toolmenu.add_command(label="Max filtering(3x3)"
                             , command=lambda: self.smoothing(img, 'Max_filtering', 1))
        toolmenu.add_command(label="peak filtering(3x3)"
                             , command=lambda: self.smoothing(img, 'peak_filter', 1))
        toolmenu.add_command(label="valley filtering(3x3)"
                             , command=lambda: self.smoothing(img, 'valley_filter', 1))

        self.master.config(menu=self.menubar)

        self.label = Label(self)
        self.label["text"] = "Process: "
        self.label["font"] = "Courier, 20"
        self.label["width"] = 60
        self.label.grid(row=0, column=0)

    # read and show the image
    def readImage(self):
        filename = tkFileDialog.askopenfilename(title="open", filetypes=[("Image Files", '*.jpg;*.jpeg;*.png')])
        global img
        global originImg
        img = cv2.imread(filename)
        gray = self.rgb2gray(img)
        img = gray
        originImg = np.copy(img)

        self.label["text"] = "Process: "

        global panelA, panelB
        image = Image.fromarray(img)
        width = 350
        ratio = float(width) / image.size[0]
        height = int(image.size[1] * ratio)
        image.thumbnail((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", anchor=SW, padx=10, pady=10)
            panelB = Label(image=image)
            panelB.image = image
            panelB.pack(side="right", anchor=SE, padx=10, pady=10)
        else:
            panelA.configure(image=image)
            panelA.image = image
            panelB.configure(image=image)
            panelB.image = image

    def reset(self):
        global img
        global originImg
        global panelA, panelB
        img = np.copy(originImg)

        image = Image.fromarray(img)
        width = 350
        ratio = float(width) / image.size[0]
        height = int(image.size[1] * ratio)
        image.thumbnail((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.label["text"] = "Process: "
        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", anchor=SW, padx=10, pady=10)
            panelB = Label(image=image)
            panelB.image = image
            panelB.pack(side="right", anchor=SE, padx=10, pady=10)
        else:
            panelA.configure(image=image)
            panelA.image = image
            panelB.configure(image=image)
            panelB.image = image

    def addNoise(self, type):
        global img
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                ran = random.random()
                if type == 0:
                    if 0.85 > ran >= 0.7:
                        img.itemset((i, j, 0), 0)
                        img.itemset((i, j, 1), 0)
                        img.itemset((i, j, 2), 0)
                    elif ran >= 0.85:
                        img.itemset((i, j, 0), 255)
                        img.itemset((i, j, 1), 255)
                        img.itemset((i, j, 2), 255)
                elif type == 1:
                    if ran >= 0.7:
                        img.itemset((i, j, 0), 0)
                        img.itemset((i, j, 1), 0)
                        img.itemset((i, j, 2), 0)
                elif type == 2:
                    if ran >= 0.7:
                        img.itemset((i, j, 0), 255)
                        img.itemset((i, j, 1), 255)
                        img.itemset((i, j, 2), 255)

        global panelA
        image = Image.fromarray(img)
        width = 350
        ratio = float(width) / image.size[0]
        height = int(image.size[1] * ratio)
        image.thumbnail((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        if panelA is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="right", anchor=SW, padx=10, pady=10)
        else:
            panelA.configure(image=image)
            panelA.image = image

    def rgb2gray(self, rgb):
        for i in range(0, rgb.shape[0]):
            for j in range(0, rgb.shape[1]):
                gray = 0.2989 * rgb.item(i, j, 0) + 0.5870 * rgb.item(i, j, 1) + 0.1140 * rgb.item(i, j, 2)
                rgb.itemset((i, j, 0), gray)
                rgb.itemset((i, j, 1), gray)
                rgb.itemset((i, j, 2), gray)
        return rgb

    def smoothing(self, gray, type, mask):
        if gray is None:
            tkMessageBox.showinfo("Message", "Please press 'open' button first")
        else:
            result = np.copy(gray)
            for i in range(0, gray.shape[0]):
                for j in range(0, gray.shape[1]):
                    # neighborhood averaging
                    if type == 'neighborhood_averaging':
                        change = self.neighborhoodAveraging(gray, i, j, mask)
                    # median filtering
                    elif type == 'median_filtering':
                        change = self.medianFiltering(gray, i, j, mask)
                    # Bilateral filter
                    elif type == 'Bilateral_filter':
                        change = self.BilateralFilter(gray, i, j, mask, 50, 3)
                    # Min filtering
                    elif type == 'Min_filtering':
                        change = self.minFiltering(gray, i, j, mask)
                    # Max/Min filtering
                    elif type == 'Max_filtering':
                        change = self.maxFiltering(gray, i, j, mask)
                    # peak filtering
                    elif type == 'peak_filter':
                        change = self.peakFilter(gray, i, j, mask)
                    # valley filtering
                    elif type == 'valley_filter':
                        change = self.valleyFilter(gray, i, j, mask)

                    result.itemset((i, j, 0), change)
                    result.itemset((i, j, 1), change)
                    result.itemset((i, j, 2), change)
            if len(self.label["text"]) % 70 >= 50:
                self.label["text"] += "\n"
            self.label["text"] += type + "(" + str(mask * 2 + 1) + "x" + str(mask * 2 + 1) + ") ->"

            global img
            img = np.copy(result)

            global panelB
            image = Image.fromarray(result)
            width = 350
            ratio = float(width) / image.size[0]
            height = int(image.size[1] * ratio)
            image.thumbnail((width, height), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            if panelB is None:
                panelB = Label(image=image)
                panelB.image = image
                panelB.pack(side="right", anchor=SE, padx=10, pady=10)
            else:
                panelB.configure(image=image)
                panelB.image = image

    def neighborhoodAveraging(self, gray, x, y, m):
        average = 0
        total = 0
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    average += gray.item(x + i, y + j, 0)
                    total += 1
        return average / total

    def medianFiltering(self, gray, x, y, m):
        mylist = []
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    mylist.append(gray.item(x + i, y + j, 0))
        return np.median(mylist)

    def BilateralFilter(self, gray, x, y, m, sigmaColor, sigmaSpace):
        sum = 0
        result = 0
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    colorTemp = self.colorGauss(gray.item(x, y, 0), gray.item(x + i, y + j, 0), sigmaColor)
                    spaceTemp = self.spaceGauss(x, y, x + i, y + j, sigmaSpace)
                    result += gray.item(x + i, y + j, 0) * colorTemp * spaceTemp
                    sum += colorTemp * spaceTemp
        return result / sum

    def colorGauss(self, l1, l2, sigmaColor):
        return math.exp(- ((l1 - l2) ** 2) / (2 * (sigmaColor ** 2)))

    def spaceGauss(self, x1, y1, x2, y2, sigmaSpace):
        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return math.exp(- d ** 2 / (2 * sigmaSpace ** 2))

    def minFiltering(self, gray, x, y, m):
        mylist = []
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    mylist.append(gray.item(x + i, y + j, 0))
        return min(mylist)

    def maxFiltering(self, gray, x, y, m):
        mylist = []
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    mylist.append(gray.item(x + i, y + j, 0))
        return max(mylist)

    def peakFilter(self, gray, x, y, m):
        mylist = []
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    mylist.append(gray.item(x + i, y + j, 0))
        mylist.sort(reverse=True)
        if mylist[0] == gray.item(x, y, 0):
            return mylist[1]
        else:
            return gray.item(x, y, 0)

    def valleyFilter(self, gray, x, y, m):
        mylist = []
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                if (gray.shape[0] - 1) >= (x + i) >= 0 and (gray.shape[1] - 1) >= (y + j) >= 0:
                    mylist.append(gray.item(x + i, y + j, 0))
        mylist.sort()
        if mylist[0] == gray.item(x, y, 0):
            return mylist[1]
        else:
            return gray.item(x, y, 0)

if __name__ == '__main__':
    root = Tk()
    panelA = None
    panelB = None
    root.resizable(width=False, height=False)
    root.minsize(width=800, height=600)
    root.title("Smoothing of Image Processing")
    app = Main(master=root)
    app.mainloop()
