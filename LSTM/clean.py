#!/usr/bin/python
# -*- coding: UTF-8 -*- 

from pandas import read_csv
from datetime import datetime

def parse(x):
    return datetime.strptime(x, '%Y %m %d %H')#时间格式解析函数
#vscode下不能从源码文件所在寻找文件，需要从工作目录进入
dataset = read_csv('./PWS/LSTM/GuangzhouPM20100101_20151231.csv',  parse_dates = [['year', 'month', 'day', 'hour']], index_col=0, date_parser=parse)
#parse_dates列已被使用解析函数替换
dataset.drop('No', axis=1, inplace=True)#编号
dataset.drop('PM_City Station', axis=1, inplace=True)
dataset.drop('PM_US Post', axis=1, inplace=True)#US Department of State Air Quality Monitoring Program
dataset.drop('PM_5th Middle School', axis=1, inplace=True)
dataset.drop('DEWP', axis=1, inplace=True)#露点
dataset.drop('precipitation', axis=1, inplace=True)#降水量/小时
dataset.drop('Iprec', axis=1, inplace=True)#累计降水量
dataset.drop('cbwd', axis=1, inplace=True)#组合风'''
print(dataset.head(5))
dataset.to_csv('clean.csv')
#余下列：时间   季节    湿度（%）    气压（hPa）    温度（℃）    风速（m/s）'''