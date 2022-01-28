import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy
import tensorflow as tf
from keras.models import load_model
import os
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
from os.path import exists
from datetime import date
import time
from csv import DictWriter

class lstm_predict():

	def __init__(self, dataset_path, model_path, pred_path):
		self.model_path = model_path
		self.dataset_path = dataset_path
		self.pred_path = pred_path
		#self.logger = logger

	def preprocess(self,df1):
    
	    
	    df1 =df1.drop(['date'],axis=1)
	    df1 = df1.dropna(axis=0,how = 'all')
	    train_dates = pd.to_datetime(df1['time'])
	    
	    cols = list(df1)[1:]
	    df_train =df1[cols].astype(float)
	    scalar = MinMaxScaler()
	    scalar = scalar.fit(df_train)
	    df_scaled = scalar.transform(df_train)
	    trainx =[]
	    trainy =[]
	    nfuture = 1
	    npast = 4
	    
	    for i in range(4,0,-1):
	        trainx.append(df_scaled[len(df_scaled)-i])
	      
	    trainx = numpy.array(trainx)
	    trainx = numpy.expand_dims(trainx,0)
	    print(trainx.shape)
	    
	    return trainx,scalar,df_scaled.shape[1],cols


	def predict(self):

		print("Prediction triggered")

		model = load_model(self.model_path)
		df=pd.read_csv(self.dataset_path)

		if(len(df)>=4):
			trainx,scalar,cons,cols = self.preprocess(df)
			train_predict=model.predict(trainx)
			copies = numpy.repeat(train_predict,cons,axis=-1)
			solar_predict = scalar.inverse_transform(copies)[:,len(cols)-1]
			temp_predict = scalar.inverse_transform(copies)[:,len(cols)-2]
			solar = solar_predict.tolist()
			temp = temp_predict.tolist()

			return temp,solar

		else:
			return [0],[0]

		print("Data predicted.........")

		


	def predict_value(self):
		
		temp,solar= self.predict()

		if(solar[0]<0):
			solar[0] = 0.0

		field_names = ['time','temperature','solar_predict']
	
		file_path = self.pred_path
		value = time.time()+900
		value = time.strftime("%H:%M:%S", time.localtime(value))

		json_data = {"time":value,"temperature":temp[0],"solar_predict":solar[0]}

		if(exists(file_path)):
			with open(file_path, 'a') as f_object:
				dictwriter_object = DictWriter(f_object, fieldnames=field_names)
				dictwriter_object.writerow(json_data)
				f_object.close()
		else:
			with open(file_path, 'w') as f_object:
				dictwriter_object = DictWriter(f_object, fieldnames=field_names)
				dictwriter_object.writeheader()
				dictwriter_object.writerow(json_data)
				f_object.close()

		print("data logged.....")






