import cv2
import os
import shutil
import numpy as np

class OpencvAlign:
    def __init__(self,imagePath):
        self.imagePath = imagePath
        self.image = cv2.imread(imagePath)
        self.faces = []

    def Cut(self):
        casc_path = './haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(casc_path)
        self.faces = face_cascade.detectMultiScale(
            self.image,
            scaleFactor=1.25,
            minNeighbors=2,
            minSize=(30, 30),
        )
        print ('Found {0} faces!'.format(len(self.faces)) )
        #self.Resize()
        cv2.imwrite('./out/'+ self.imagePath , self.image)

    def Resize(self):
        for (x, y, w, h) in self.faces:
            cutImg = self.image[y:y + h,x:x + w]
            resizeImg = cv2.resize(cutImg,(168,168)) 
            cv2.imwrite('./out/'+ self.imagePath , resizeImg)


