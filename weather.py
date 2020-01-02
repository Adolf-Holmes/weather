#%%
class weather:
    humi=0.0#湿度
    pres=0.0#气压
    temp=0.0#温度
    wdsd=0.0#风速
    PM25=0.0#PM2.5
    def to_WU_dict(self):
        import PWS.Weather_Underground as wu
        wu_dict = {'humidity':self.humi,'tempf':wu.degc_to_degf(self.temp),'dewptf':wu.degc_to_degf(wu.cal_dewp(self.humi,self.temp)),'baromin':wu.hpa_to_inches(self.pres),'windspeedmph':wu.kmph_to_nph(self.wdsd),'AqPM2.5':self.PM25}
        return wu_dict
# %%
w=weather()
di=w.to_WU_dict()
print(di)


# %%
