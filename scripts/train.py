import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import numpy
import tensorflow as tf
from tensorflow.keras.layers import Dropout
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Bidirectional
from keras.models import load_model
import os
import matplotlib.pyplot as plt


class lstm_train():
	
	def __init__(self, dataset_path, model_path):
		self.model_path = model_path
		self.dataset_path = dataset_path



	def loadmodel(self,trainx,trainy):

	    if(os.path.exists(self.model_path)):
	        model =load_model(self.model_path)
	        print("model loaded")
	    else:

	        model = Sequential()
	        model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(trainx.shape[1],trainx.shape[2])))
	        model.add(Dense(trainy.shape[1]))
	        model.compile(optimizer='adam', loss='mse')
	        model.summary()
	        
	    return model


	def preprocess(self,filepath):
    
	    df=pd.read_csv(filepath)
	    df1 =df.drop(['date'],axis=1)  
	    
	    train_dates = pd.to_datetime(df['time'])
	    
	    cols = list(df1)[1:]
	    df_train =df1[cols].astype(float)
	    scalar = MinMaxScaler()
	    scalar = scalar.fit(df_train)
	    df_scaled = scalar.transform(df_train)
	    trainx =[]
	    trainy =[]
	    nfuture = 1
	    npast = 4

	    for i in range(npast,len(df_scaled)-nfuture+1):
	        trainx.append(df_scaled[i-npast:i,0:df_scaled.shape[1]])
	        trainy.append(df_scaled[i+nfuture-1:i+nfuture,len(cols)-1])
	        
	    trainx,trainy = numpy.array(trainx),numpy.array(trainy)
	    print(trainx.shape)
	    
	    return trainx,trainy,scalar,df_scaled.shape[1],cols


	def train(self,filepath):
    
	    trainx,trainy,scalar,cons,cols = self.preprocess(filepath)
	    print(trainx.shape)
	    model = self.loadmodel(trainx,trainy)
	    history = model.fit(trainx,trainy,validation_split =0.1,epochs=100,batch_size=16,verbose=0)
	    
	    model.save(self.model_path)
	    
	    return history


	def train_network(self):

		for i,(dirpath,dirname,filename) in enumerate(os.walk(self.dataset_path)):
			for f in filename:
				file = str(dirpath+"/"+f)
				history = self.train(file)
				print("Data trained successfully")


		plt.plot(history.history['loss'],label ='Training loss')
		plt.plot(history.history['val_loss'],label ='Validation loss')
		plt.legend()

		return 0



	    