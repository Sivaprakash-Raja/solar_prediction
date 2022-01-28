import requests
import time
import paho.mqtt.client as mqttClient
import json
import urllib.parse



class weather:

	def __init__(self,location):

		self.address = location
		self.response = requests.get('https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(self.address) +'?format=json').json()
		self.latitude = self.response[0]["lat"]
		self.longditude = self.response[0]["lon"]
		self.api_key = "da795f6d4917fc9cbe5ccd9454267fe6"
		self.exclude_current = "hourly,minutely,alerts,daily"
		self.exclude_hour = "current,minutely,alerts,daily"



	def get_current_weather(self):

		
		res = requests.get( f'https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longditude}&exclude={self.exclude_current}&appid={self.api_key}' ).json()

		data = res["current"]

		json_data = {"date" :time.strftime('%d-%m-%Y', time.localtime(data["dt"])),"time" : time.strftime('%H:%M:%S', time.localtime(data["dt"])),"temp": data["temp"]-273.15,"pressure" :data["pressure"]*100,"humidity": data["humidity"],"uv_index" : data["uvi"],"clouds_percentage" : data["clouds"],"visibility" : data["visibility"],"wind_speed": data["wind_speed"],"wind_deg": data["wind_deg"]}

		return json_data







	





