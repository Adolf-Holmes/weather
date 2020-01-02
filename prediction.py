#%%定义
from math import sqrt
from numpy import concatenate
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
#%%
#季节   相对湿度    气压    温度    风速
dataset = read_csv('./PWS/LSTM/pred.csv', header=0, index_col=0)#至少需要三个小时的数据
values = dataset.values

'''# 整数编码
encoder = LabelEncoder()
values[:,0] = encoder.fit_transform(values[:,0])
# ensure all data is float 确保所有数据是浮动的'''
values = values.astype('float32')
print(values)
# 归一化特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
print(scaled)
# 构建监督学习问题
# 指定滞后时间大小
n_hours = 3#预测所需小时数
reframed = series_to_supervised(scaled,n_hours-1, 1)#预测没有实际值
# 丢弃我们并不想预测的列
#reframed.drop(reframed.columns[], axis=1, inplace=True)
print(reframed)
# %% 分割
values = reframed.values
test = values[:, :]
n_features = 4
n_obs = n_hours * n_features
test_X = test[:, :n_obs]
print(test_X)
# %%
model = tf.keras.models.load_model('air_analysis.model')
hour = 4#预测四个小时的数据
for i in range(0,hour-1):
    test_X = test[n_features*i:,:]
    test_X = test_X.reshape((test_X.shape[0], n_hours,n_features))
    yhat = model.predict(test_X)
    print(yhat)
    test += yhat
    inv_yhat = scaler.inverse_transform(yhat)
    print(inv_yhat)
# %%
