import paho.mqtt.client as mqttClient
import json
import time
from os.path import exists
import os

class Mqtt:

	def __init__(self):
		self.json_data = {}
		self.path = "C:\\Users\\shiva\\OneDrive\\Desktop\\Projects\\Short-term solar power forecasting\\Version 1\\var\\"
		mqttclient = mqttClient.Client("5664127898765")
		mqttclient.on_connect = self.on_connect
		mqttclient.on_message = self.on_message
		mqttstatus = mqttclient.connect("broker.emqx.io", 1883,60)
		mqttclient.loop_forever()

	def on_connect(self,mqttclient, userdata, flags,rc):
		if rc == 0:
			mqttclient.subscribe("/test/weather")
			print("Connected")
		else:
			print("Connection failed")
        
	def on_message(self,mqttclient, userdata, msg):
	
		mqtt_msg = str(msg.payload).replace("\n", "").replace("b'", "").replace("'", "")
		json_data = json.loads(mqtt_msg)

		wdata = {"temperature":json_data["data"]["Temperature"],"solar_irradiation":json_data["data"]["Solar_Irradiation"]}

		print(wdata)

		with open(self.path+"config.json", "w") as jsonFile:
			json.dump(wdata, jsonFile)	
		print("done")

		



Mqtt()

