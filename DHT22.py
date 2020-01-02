import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
GPIO=18#gpio编号，而不是pin口编号
sensor_dht = Adafruit_DHT.DHT22
sensor_bmp = BMP085.BMP085()
humidity, ambient_temp = Adafruit_DHT.read_retry(sensor_dht, GPIO)
pressure = sensor_bmp.read_pressure()/100
humidity="{0:.2f}".format(humidity)
ambient_temp="{0:.2f}".format(ambient_temp)
pressure="{0:.2f}".format(pressure)
