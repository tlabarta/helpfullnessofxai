import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import gzip

import keras
from keras.layers import Input,Conv2D,MaxPooling2D,UpSampling2D,Flatten,Dense
from keras.models import Model, load_model
from tensorflow.keras.optimizers import RMSprop, Adam
from keras.applications.vgg16 import VGG16



class Autoencoder():
    
    def __init__(self, load_path=None):
        
        if load_path:
            self.autoencoder = load_model(load_path)
        else:
            input_image = Input(shape = (224, 224, 3))
            self.autoencoder=Model(input_image, self.mymodel1(input_image))
            self.autoencoder.compile(loss='mean_squared_error', optimizer = Adam())
            self.autoencoder.summary()

    def mymodel1(self, input_img, TRAINABLE=False):

        base_model = VGG16(weights='imagenet')

        for layer in base_model.layers:
            layer.trainable=TRAINABLE

    #-------------------encoder---------------------------- 
    #--------(pretrained & trainable if selected)----------

    #    block1
        x=base_model.get_layer('block1_conv1')(input_img)
        x=base_model.get_layer('block1_conv2')(x)
        x=base_model.get_layer('block1_pool')(x)

    #    block2
        x=base_model.get_layer('block2_conv1')(x)
        x=base_model.get_layer('block2_conv2')(x)
        x=base_model.get_layer('block2_pool')(x)

    #    block3
        x=base_model.get_layer('block3_conv1')(x)
        x=base_model.get_layer('block3_conv2')(x)
        x=base_model.get_layer('block3_conv3')(x)    
        x=base_model.get_layer('block3_pool')(x)

    #    block4
        x=base_model.get_layer('block4_conv1')(x)
        x=base_model.get_layer('block4_conv2')(x)
        x=base_model.get_layer('block4_conv3')(x)    
        x=base_model.get_layer('block4_pool')(x)

    #    block5
        x=base_model.get_layer('block5_conv1')(x)
        x=base_model.get_layer('block5_conv2')(x)
        x=base_model.get_layer('block5_conv3')(x)


    #--------latent space (trainable) ------------
        x=base_model.get_layer('block5_pool')(x)     
        x = Conv2D(512, (3, 3), activation='relu', padding='same',name='latent')(x)
        x = UpSampling2D((2,2))(x)  

    #--------------decoder (trainable)----------- 

      # Block 5
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv1')(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv2')(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock5_conv3')(x)
        x = UpSampling2D((2,2))(x)

      # Block 4
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv1')(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv2')(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='same', name='dblock4_conv3')(x)
        x = UpSampling2D((2,2))(x)

      # Block 3
        x = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv1')(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv2')(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='same', name='dblock3_conv3')(x)
        x = UpSampling2D((2,2))(x)     

      # Block 2
        x = Conv2D(128, (3, 3), activation='relu', padding='same', name='dblock2_conv1')(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='same', name='dblock2_conv3')(x)
        x = UpSampling2D((2,2))(x)        

      # Block 1
        x = Conv2D(64, (3, 3), activation='relu', padding='same', name='dblock1_conv1')(x)
        x = Conv2D(3, (3, 3), activation='relu', padding='same', name='dblock1_conv3')(x)
    #    x = UpSampling2D((2,2))(x) 

        return x
    
    def fit(self, data_path, epochs=10, use_multiprocessing=False):
        # a small toy dataset from imagenet
        x=np.load(data_path)
        # normalize
        x = x / 255
        x_train,x_val = train_test_split(x, test_size=0.2, random_state=123)
        self.autoencoder.fit(x_train, x_train, batch_size=32,epochs=epochs,verbose=1,validation_data=(x_val, x_val), use_multiprocessing=use_multiprocessing)
        
    def predict(self, x):
        return self.autoencoder.predict(x)
        
    def save(self, path):
        self.autoencoder.save(path, save_format='h5')
    
    def __call__(self, data):
        return self.autoencoder(data)[0]
        