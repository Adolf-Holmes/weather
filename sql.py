#%%
import sqlite3
conn=sqlite3.connect(':memory:')
def sqlinsert(weather):
    import PWS.weather
    sql = conn.cursor()
    sql.execute("INSERT INTO weather VALUES(NULL,datetime('now', 'localtime'),?,?,?,?,?)",(weather.humi,weather.pres,weather.temp,weather.wdsd,weather.PM25))
def sqlread():
    from pandas import DataFrame
    from pandas import read_sql
    #con = sqlite3.connect('weather.db')
    date = read_sql('SELECT * from weather',conn)
    return date
if __name__ == '__main__':
    import PWS.weather
    w=PWS.weather.weather()
    w.humi=75.0
    w.pres=1026.0
    w.temp=17.0
    w.wdsd=6.0
    w.PM25=60
    c = conn.cursor()
    c.execute('''CREATE TABLE weather
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       datatime DATATIME NOT NULL,
       HUMI FLOAT,PRES FLOAT,TEMP FLOAT,Iws FLOAT,PM25 FLOAT);''')
    sqlinsert(w)
    cursor = c.execute("SELECT * from weather")
    for row in cursor:
        for i in range(0,6):
            print(row[i])
    date=DataFrame()
    date=sqlread()
    print(sqlread())
# %%
