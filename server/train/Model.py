import numpy as np  
from numpy  import array
import pandas as pd
from keras.models import Sequential  
from keras.optimizers import RMSprop , Adam
from keras.layers import GaussianNoise, Dense , Conv2D , Activation , Dropout , Flatten , BatchNormalization , Reshape , UpSampling2D ,Conv2DTranspose,MaxPooling2D
import matplotlib.pyplot as plt
from keras.layers.advanced_activations import LeakyReLU
from keras.layers import Input
from keras.utils import np_utils
from keras.models import Model
import h5py
import os
from os import listdir
from os.path import isfile, isdir, join
from keras import backend as K
from PIL import Image
import sys
import keras 
import random
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import time


from keras.engine.topology import Layer
class InstanceNormalization2D(Layer):
    def __init__(self,
                 beta_initializer='zeros',
                 gamma_initializer='ones',
                 epsilon=1e-3,
                 **kwargs):
        super(InstanceNormalization2D, self).__init__(**kwargs)
        if K.image_data_format() is 'channels_first':
            self.axis = 1
        else: # image channels x.shape[3]
            self.axis = 3
        print()
        self.epsilon = epsilon
        self.beta_initializer = beta_initializer
        self.gamma_initializer = gamma_initializer

    def build(self, input_shape):
        self.gamma = self.add_weight(shape=(input_shape[self.axis],),
                                     initializer=self.gamma_initializer,
                                     trainable=True,
                                     name='gamma')
        self.beta = self.add_weight(shape=(input_shape[self.axis],),
                                    initializer=self.beta_initializer,
                                    trainable=True,
                                    name='beta')
        super(InstanceNormalization2D, self).build(input_shape)

    def call(self, x):
        # spatial dimensions of input
        if K.image_data_format() is 'channels_first':
            x_w, x_h = (2, 3)
        else:
            x_w, x_h = (1, 2)

        # Very similar to batchnorm, but normalization over individual inputs.

        hw = K.cast(K.shape(x)[x_h]* K.shape(x)[x_w], K.floatx())

        # Instance means
        mu = K.sum(x, axis=x_w)
        mu = K.sum(mu, axis=x_h)
        mu = mu / hw
        mu = K.reshape(mu, (K.shape(mu)[0], K.shape(mu)[1], 1, 1))

        # Instance variences
        sig2 = K.square(x - mu)
        sig2 = K.sum(sig2, axis=x_w)
        sig2 = K.sum(sig2, axis=x_h)
        sig2 = K.reshape(sig2, (K.shape(sig2)[0], K.shape(sig2)[1], 1, 1))

        # Normalize
        y = (x - mu) / K.sqrt(sig2 + self.epsilon)

        # Scale and Shift
        if K.image_data_format() is 'channels_first':
            gamma = K.reshape(self.gamma, (1, K.shape(self.gamma)[0], 1, 1))
            beta = K.reshape(self.beta, (1, K.shape(self.beta)[0], 1, 1))
        else:
            gamma = K.reshape(self.gamma, (1, 1, 1, K.shape(self.gamma)[0]))
            beta = K.reshape(self.beta, (1, 1, 1, K.shape(self.beta)[0]))
        return gamma * y + beta

def normalize(**kwargs):
    return InstanceNormalization2D()

batch_size = 12;
pixel = 168

def ReadImg(path):
    imglist = []
    files = listdir(path)
    for f in files:
        f2 = join(path, f)
        img = Image.open(f2)
        img = img.resize((pixel, pixel), Image.ANTIALIAS)
        img = np.array(img)
        o = np.ones(img.shape)
        img = img - (o * 127.5) 
        img = img / 127.5
        img=img
        imglist.append(img)
    return imglist;

def ReadImgSimple(path):
    imglist = []
    filelist = []
    filelist.append(path)
    img = Image.open(path)
    img = img.resize((168, 168), Image.ANTIALIAS)
    img = np.array(img)
    o = np.ones(img.shape)
    img = img - (o * 127.5) 
    img = img / 127.5
    img=img
    imglist.append(img)
    return imglist;

def MakeD():
    x = Input(shape=(pixel, pixel, 3))
    y = Conv2D(64, (5, 5), padding='same',strides=(2, 2))(x)
    #y = Activation('relu')(y)
    y=LeakyReLU(alpha=0.2)(y)
    y = Conv2D(128, (3, 3), padding='same',strides=(2, 2))(y)
    #y = Activation('relu')(y)
    y=LeakyReLU(alpha=0.2)(y)
    y = Conv2D(256, (3, 3), padding='same',strides=(2, 2))(y)
    #y = Activation('relu')(y)
    y=LeakyReLU(alpha=0.2)(y)
    y = Flatten()(y)
    y = Dense(512)(y)
    y = Dense(1)(y)
    y = Activation('sigmoid')(y)
    return Model(x,y)

def MakeEncoder():
   #ENCODE
    x = Input(shape=(pixel, pixel, 3))
    y = Conv2D(64, (7, 7), padding='same',strides=(1, 1))(x)
    y = normalize()(y)
    y = Activation('relu')(y)
   # y=LeakyReLU(alpha=0.2)(y)
    y = Conv2D(128, (3, 3), padding='same',strides=(2, 2))(y)
    y = normalize()(y)
    y = Activation('relu')(y)
   # y=LeakyReLU(alpha=0.2)(y)
    y = Conv2D(256, (3, 3), padding='same',strides=(2, 2))(y)
    y = normalize()(y)
   # y=LeakyReLU(alpha=0.2)(y)
    y = Activation('relu')(y)
    model = Model(inputs=x, outputs=y)
    return model

encoder = MakeEncoder();
encoder.summary()

def resnet_blocks ( input_res , num_features ) :
    x = input_res
    out_res_1 = Conv2D(num_features, (3, 3), padding='same',activation='relu',strides=(1, 1))(x)
    out_res_2 = normalize()(out_res_1)
    out_res_3 = Conv2D(num_features, (3, 3), padding='same',strides=(1, 1))( out_res_2)
    z = keras.layers.add([x, out_res_3])
    return  z

def MakeG():
    x = Input(shape=(pixel, pixel, 3))
    y = encoder(x)
    #RES
    r1 = resnet_blocks(y,256)
    r2 = resnet_blocks(r1,256)
    r3 = resnet_blocks(r2,256)
    r4 = resnet_blocks(r3,256)
    r5 = resnet_blocks(r4,256) 
    r6 = resnet_blocks(r5,256)
    #DECODE
    d = Conv2DTranspose(128, (4, 4),strides=(2),padding='same')(r6)
    d = normalize()(d)
    d = Activation('relu')(d)
    d = Conv2DTranspose(64, (4, 4),strides=(2),padding='same')(d)
    d = normalize()(d)
    d = Activation('relu')(d)
    d = Conv2D(3, (7, 7), padding='same',strides=(1, 1))(d)
    d = keras.layers.add([x, d])
    d = Activation('tanh')(d)     
    model = Model(inputs=x, outputs=d)
    return model

def poolinit():
  global imagepoolA
  global imagepoolB
  FakeX = random.sample(imglistB,int(poolsize))
  FakeX = modelGBA.predict(np.asarray(FakeX))
  imagepoolA=np.asarray(FakeX)
  FakeX = random.sample(imglistA,int(poolsize))
  FakeX = modelGAB.predict(np.asarray(FakeX))
  imagepoolB=np.asarray(FakeX)

def createimage(n):
  global imagepoolA
  global imagepoolB
  imagepoolA = imagepoolA[n:poolsize]
  FakeX = random.sample(imglistB,int(n))
  FakeX = modelGBA.predict(np.asarray(FakeX))
  imagepoolA = np.vstack((imagepoolA,np.asarray(FakeX)))
  
  imagepoolB = imagepoolB[n:poolsize]
  FakeX = random.sample(imglistA,int(n))
  FakeX = modelGAB.predict(np.asarray(FakeX))
  imagepoolB = np.vstack((imagepoolB,np.asarray(FakeX)))

def poola(n,pa):
  global imagepoolA
  global imagepoolB
  imagepoolA = imagepoolA[n:poolsize]
  FakeX = random.sample(pa,int(n))
  FakeX = modelGBA.predict(np.asarray(FakeX))
  imagepoolA = np.vstack((imagepoolA,np.asarray(FakeX)))

def poolb(n,pb):
  global imagepoolA
  global imagepoolB
  imagepoolB = imagepoolB[n:poolsize]
  FakeX = random.sample(pb,int(n))
  FakeX = modelGAB.predict(np.asarray(FakeX))
  imagepoolB = np.vstack((imagepoolB,np.asarray(FakeX)))

def TrainDA():
    RealX = random.sample(imglistA,int(batch_size/2)) 
    RealY = np.ones([int(batch_size/2), 1])
    RealY = RealY  * 0.85
    FakeY = np.zeros([int(batch_size/2), 1])
    gauss = np.random.normal(0,0.08,(int(batch_size/2),96,96,3))
    RealGX = np.asarray(RealX) + gauss
    gauss = np.random.normal(0,0.08,(int(batch_size/2),96,96,3))
    FakeGX = imagepoolA[np.random.choice(poolsize, int(batch_size/2))] + gauss
    d_lossR = modelDA.train_on_batch(RealGX, RealY)
    print ("DAR")
    print (d_lossR)
    d_lossF = modelDA.train_on_batch(FakeGX, FakeY)
    print ("DAF")
    print (d_lossF)
    d_loss =  (d_lossR[0] +  d_lossF[0]) / 2
    d_loss_record.append(d_loss)
    dR_loss_record.append(d_lossR[0])
    dF_loss_record.append(d_lossF[0])
    return d_loss

def TrainDB():
    RealX = random.sample(imglistB,int(batch_size/2)) 
    RealY = np.ones([int(batch_size/2), 1])
    RealY = RealY  * 0.85
    FakeY = np.zeros([int(batch_size/2), 1])
    gauss = np.random.normal(0,0.08,(int(batch_size/2),96,96,3))
    RealGX = np.asarray(RealX) + gauss
    gauss = np.random.normal(0,0.08,(int(batch_size/2),96,96,3))
    FakeGX = imagepoolB[np.random.choice(poolsize, int(batch_size/2))] + gauss
    d_lossR = modelDB.train_on_batch(RealGX, RealY)
    print ("DBR")
    print (d_lossR)
    d_lossF = modelDB.train_on_batch(FakeGX, FakeY)
    print ("DBF")
    print (d_lossF)
    d_loss =  (d_lossR[0] +  d_lossF[0]) / 2
    d_loss_record.append(d_loss)
    dR_loss_record.append(d_lossR[0])
    dF_loss_record.append(d_lossF[0])
    return d_loss

def TrainGA():
    OOX = random.sample(imglistA,int(batch_size))  
    OX = np.asarray(OOX) 
    FakeY = np.ones([int(batch_size), 1])
    #FakeY = FakeY  * 0.85
    a_loss = modelC1.train_on_batch(OX,[FakeY,OX])
    a_loss_record.append(a_loss[0])
    poolb(25,OOX);
    print ("GAB")
    print (a_loss)
    return 0

def TrainGB():
    OOX = random.sample(imglistB,int(batch_size))
    OX = np.asarray(OOX)
    FakeY = np.ones([int(batch_size), 1])
    #FakeY = FakeY  * 0.85
    a_loss = modelC2.train_on_batch(OX,[FakeY,OX])
    a_loss_record.append(a_loss[0])
    poola(25,OOX);
    print ("GBA")
    print (a_loss)
    return 0


