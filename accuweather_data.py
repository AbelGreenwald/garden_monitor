import json
import cayenne.client
import requests

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = ""
MQTT_PASSWORD  = ""
MQTT_CLIENT_ID = ""

# Accuweather data
API_KEY = ""
LOCATION_KEY = "2094707"
API_URL = "https://dataservice.accuweather.com/currentconditions/v1/"

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)

params = {
'apikey' : API_KEY,
'details' : True
}

#data = requests.get(API_URL + LOCATION_KEY, params=params)
#print(data.json())
#weather_data = {}

with open('Current_Conditions.json') as fh:
    weather_data = json.load(fh)

#print(weather_data)
cur_temp = weather_data[0]['Temperature']['Imperial']['Value'] #F
cur_humidity = weather_data[0]['RelativeHumidity'] #%
cur_wind_gust = weather_data[0]['WindGust']['Speed']['Imperial']['Value'] # mi/hr
rain_one_hr = weather_data[0]['PrecipitationSummary']['PastHour']['Imperial']['Value'] # in

print(cur_temp)
print(cur_humidity)
print(cur_wind_gust)
print(rain_one_hr)

client.loop()
