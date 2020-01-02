#%% 定义
import math
import requests
import http.client
def upload(weather):
    WUurl = "/weatherstation/updateweatherstation.php?"
    WU_station_id = "IZHAOQ1" # Replace XXXX with your PWS ID
    WU_station_pwd = "ma2v7BvC" # Replace YYYY with your Password
    WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
    date_str = "&dateutc=now"
    action_str = "&action=updateraw"
    get_url = WUurl + WUcreds + date_str
    for key,values in  weather.items():
        get_url += "&" + key + "=" + str(values)
    get_url += action_str
    #get_url += "&softwaretype=RaspberryPi&realtime=1&rtfreq=2.5"
    print(get_url)
    conn = http.client.HTTPSConnection("rtupdate.wunderground.com")
    conn.request("GET", get_url)
    res = conn.getresponse()
    r = res.read()
    print(r)
    #r= requests.get(get_url)
    #return "Received "+ r.status_code + " " + r.text
def hpa_to_inches(pressure_in_hpa):#气压，hPa转汞柱英寸
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m
def kmph_to_nph(win_speed_in_SI):#风速,km/s转mph(每小时英里)
    win_speed_in_UK = win_speed_in_SI * 0.621371
    return win_speed_in_UK
def mps_to_nph(win_speed_in_SI):#风速,m/s转mph(每小时英里)
    win_speed_in_UK = kmph_to_nph(win_speed_in_SI * 3.6)
    return win_speed_in_UK
def degc_to_degf(temperature_in_c):#温度,摄氏温度转华氏温度
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f
def cal_dewp(humi,temp):
    dewp = 15
    if(temp>0 and temp<60):
        a = 17.27
        b = 237.7
        GTRH = a*temp/(b+temp)+math.log(humi/100)
        dewp = a*GTRH/(b-GTRH)
    return dewp
