import json
import csv
import time
import pandas as pd
from openWeather import weather
import datetime
from csv import DictWriter
from os.path import exists
import os
from train import lstm_train
import logging
from datetime import date
from prediction import lstm_predict
#import mail

datet = str(datetime.datetime.now())
gpath = "C:\\Users\\shiva\\OneDrive\\Desktop\\Projects\\Short-term solar power forecasting\\Version 1\\"
dataset_path = gpath+"data"
model_path= gpath+"savedModel\\LSTM_model.h5"
config_path = gpath+"var\\config.json"
file_path = gpath+"var\\temp.csv"
var_path = gpath+"var"
pred_data = gpath+"var\\"
Logfile_path = gpath+"logs\\"+datet[0:11]

field_names = ['date', 'time','temp',  'pressure', 'humidity', 'uv_index', 'clouds_percentage', 'visibility', 'wind_speed', 'wind_deg', 'temperature', 'solar_irradiation']

obj = weather("madurai")
train = lstm_train(dataset_path=dataset_path,model_path=model_path)

logging.basicConfig(filename= Logfile_path,
                    format='%(asctime)s %(message)s',
                    filemode='a')
 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def prep_data():

	logger.info("reading data........")

	current_data = obj.get_current_weather()

	with open(config_path,'r') as js:
		actual_data = json.load(js)

	data = {'temperature': 0,'solar_irradiation': 0}

	if(actual_data!=data):

		with open(config_path, "w") as jsonFile:
			json.dump(data, jsonFile)

		json_data = { **current_data, **actual_data }
		logger.info(json_data)

		
		
	else :
		current_data = {"date" :0,"time" : 0,"temp": 0,"pressure" : 0,"humidity": 0,"uv_index" :0,"clouds_percentage" : 0,"visibility" : 0,"wind_speed":0,"wind_deg":0}
		json_data = { **current_data, **actual_data }
		logger.info(json_data)
		logger.debug("Check hardware connection")

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

	logger.info("data logged.....")

	return
	


def train_func():

	logger.info("Training Triggered.........")

	filename = f'{str(date.today())}.csv'
	path = dataset_path +"\\"+ filename

	df = pd.read_csv(file_path)
	df = df.dropna(axis = 0,how ='all')
	df.to_csv(path, index=False)

	logger.info("Data file restored.........")

	if(len(df)==49):
		logger.info("Training Started.........")
		status = train.train_network()
		print(f'Status code : {status}')
		logger.info("Training completed.........")
	else:
		logger.info("Training is terminated......Data not sufficient")

	return


def predict_func():
	logger.info("prediction Triggered")
	n = lstm_predict(file_path,model_path,var_path)
	n.predict_value()

	return





while(1):
	
	current_time = str(datetime.datetime.now())
	hour = int(current_time[11:13])
	minute = int(current_time[14:16])

	#data collection

	#if(hour>=0 and hour<=23):
	#	if(minute>=0 or minute==15 or minute==30 or minute==45):	
	prep_data()
	predict_func()
				
	time.sleep(60)		



	if(hour==23):
		if(minute==10):
			train_func()
			time.sleep(60)

	print("while")

	'''
	if(hour==12):
		if(minute==53):
			filename = f'{str(date.today())}_predicted.csv'

			df = pd.read_csv(pred_data+filename)
			df1 = pd.read_csv(file_path)
			sendmail(df,df1)
			break
	'''		