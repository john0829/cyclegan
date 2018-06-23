from Model import *
import tensorflow as tf
import time
import scipy.misc
import numpy

class ChangeStyle():
  def __init__(self):
    self.DA=MakeD()
    self.DB=MakeD()
    self.GAB=MakeG()
    self.GBA=MakeG()

    optimizerD = Adam(0.0002, 0.5)
    optimizerA = Adam(0.0002, 0.5)

    #DA
    self.modelDA = Sequential()
    self.modelDA.add(self.DA)
    self.modelDA.compile(loss='binary_crossentropy', optimizer=optimizerD,metrics=['accuracy'])
    self.modelDA.summary()
    #DB
    self.modelDB = Sequential()
    self.modelDB.add(self.DB)
    self.modelDB.compile(loss='binary_crossentropy', optimizer=optimizerD,metrics=['accuracy'])
    self.modelDB.summary()
    #DA
    self.modelGAB = Sequential()
    self.modelGAB.add(self.GAB)
    self.modelGAB.summary()
    #DB
    self.modelGBA = Sequential()
    self.modelGBA.add(self.GBA)
    self.modelGBA.summary()

    self.modelGAB.load_weights('./model/n-GAB-4.h5')
    global graphGAB
    graphGAB = tf.get_default_graph()
    self.modelGBA.load_weights('./model/n-GBA-4.h5')
    global graphGBA
    graphGBA = tf.get_default_graph()

  def changeToAnime(self,img_path):
    imglistB = []
    imglistB = ReadImgSimple(img_path)
    X = random.sample(imglistB,1) 
    start = time.time() 
    
    with graphGBA.as_default():
      if(img_path == "imageToSave.png"):
        Y = self.modelGBA.predict(np.asarray(X))
      else:
        print(np.asarray(X).shape)
        Y = self.modelGBA.predict(np.asarray(X))
    end = time.time()
    print("spend time :" ,end-start)

    img = Y[0]
    img = img.reshape(168,168,3)
    img = img * 0.5 + 0.5
    if(img_path == "imageToSave.png"):
      scipy.misc.imsave('outfileAnime.jpg', img)
    else:
      scipy.misc.imsave('outfileCamera.jpg', img)

  def chamgeToReal(self,img_path):
    imglistB = []
    imglistB = ReadImgSimple(img_path)
    X = random.sample(imglistB,1) 
    start = time.time() 
    with graphGBA.as_default():
      Y = self.modelGAB.predict(np.asarray(X))
    end = time.time()
    print("spend time :" ,end-start)

    img = Y[0]
    img = img.reshape(168,168,3)
    img = img * 0.5 + 0.5
    scipy.misc.imsave('outfileReal.jpg', img)
    



