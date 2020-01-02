# -*- coding: UTF-8 -*-
import Adafruit_DHT
import Adafruit_BMP.BMP085 
import serial
from PWS.weather import weather
def readweather():
    GPIO=18#gpio编号，而不是pin口编号
    ser = serial.Serial('/dev/ttyACM0', 9600,timeout=1); 
    sensor_dht = Adafruit_DHT.DHT22
    sensor_bmp = Adafruit_BMP.BMP085.BMP085()
    humidity, ambient_temp = Adafruit_DHT.read_retry(sensor_dht, GPIO)
    pressure = sensor_bmp.read_pressure()/100
    ser.write("r".encode(encoding='UTF-8',errors='strict'))
    response = ser.readall();
    response = str(response[3:-5])
    weather_dict = eval(response)
    noweather = weather()
    noweather.humi=float("{0:.2f}".format(humidity))
    noweather.temp=float("{0:.2f}".format(ambient_temp))
    noweather.pres=float("{0:.2f}".format(pressure))
    noweather.wdsd=float(weather_dict['wind_speed'])
    noweather.PM25=float(weather_dict['AqPM25'])
    ser.close()
    return noweather
if __name__ == '__main__':
    import PWS.Weather_Underground as wu
    noweather = readweather()
    wu.upload(noweather.to_WU_dict())