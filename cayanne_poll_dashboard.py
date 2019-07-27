import cayenne.client
import datetime
import time
import requests
import serial
import logging

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = ""
MQTT_PASSWORD  = ""
MQTT_CLIENT_ID = ""

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883)

i=0
timestamp = 0
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

#Start Fresh
ser.flushOutput()
ser.flushInput()

# Accuweather data
API_KEY = ""
LOCATION_KEY = "2094707"
API_URL = "https://dataservice.accuweather.com/currentconditions/v1/"

params = {
'apikey' : API_KEY,
'details' : True
}



ser.isOpen()
out = b''
moist = 0
prev_time = datetime.datetime.now() - datetime.timedelta(hours=1.1)
start_time = datetime.datetime.now()

while True:
    now_time = datetime.datetime.now()
    uptime = now_time - start_time
    client.loop()
    client.virtualWrite(0, uptime.total_seconds(), "counter", "null")
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != b'':
        b_val = out.strip()
        try:
            moist = float(b_val)
            out = b''
            if moist < 0 or moist > 100:
                raise Exception()
            if now_time >= (prev_time + datetime.timedelta(hours=1)):
                print(str(datetime.datetime.now()) + ": Polling weather data")
                response = requests.get(API_URL + LOCATION_KEY, params=params)
                weather_data = response.json()
                cur_temp = weather_data[0]['Temperature']['Imperial']['Value'] #F
                cur_humidity = weather_data[0]['RelativeHumidity'] #%
                cur_wind_gust = weather_data[0]['WindGust']['Speed']['Imperial']['Value'] # mi/hr
                rain_one_hr = weather_data[0]['PrecipitationSummary']['Past24Hours']['Imperial']['Value'] # in
                prev_time = datetime.datetime.now()
            client.virtualWrite(1, moist, "moisture", "%")
            client.virtualWrite(2, rain_one_hr, "rain_level", "inches")
            client.virtualWrite(3, cur_humidity, "rel_hum", "%")
            client.virtualWrite(4, cur_temp, "temp", "f")
            client.virtualWrite(5, cur_wind_gust, "wind_speed", "mph")
        except Exception as e:
            print("Error parsing serial data: " + str(b_val))
            print(e)
            ser.flushOutput()
            ser.flushInput()
    time.sleep(15)
