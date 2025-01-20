import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

#create a class for more readable of my code
class BitPlaneExtraction:
    
    def __init__(self, img_path):#constructor of BitPlaneExtraction class
        self.img_path = img_path
        self.img = cv2.imread(img_path, 0)
        self.bitplanes = []
        for i in range(8):#split image to bitlanes
            Ib = np.uint8(cv2.bitwise_and(self.img, 2**i))
            self.bitplanes.append(Ib)
    
    def extract_text(self):#method for extract secret message 
        #create variables
        is_calculating = True
        row, col = 0, 0
        temp = ""
        #main loop is look all bits and translate it
        while is_calculating:
            time.sleep(0.01)#use time for more userfriendly output (doesn't need it)
            temp += str(self.bitplanes[0][row][col])#temp takes all bits in wanted order (strategy2)
            row += 1
            if row == 256:
                row = 0
                col += 1
            ascii_str = ''.join(chr(int(temp[i:i+8], 2)) for i in range(0, len(temp), 8))#translate 8bit to ascii
            if ascii_str[-1] == '#':#when it sees # it will stop
                is_calculating = False
            print(ascii_str)

#use this for more readability
if __name__ == "__main__":
    text_extractor = BitPlaneExtraction("05.tif")
    text_extractor.extract_text()