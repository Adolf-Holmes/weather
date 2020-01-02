# %% 数据处理，构造为监督学习
from math import sqrt
from numpy import concatenate
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
# 转换序列成监督学习问题
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

# 加载数据集
dataset = read_csv('./PWS/LSTM/clean.csv', header=0, index_col=0)
print(dataset)
values = dataset.values
print(values)
# 整数编码
#encoder = LabelEncoder()
#values[:,0] = encoder.fit_transform(values[:,0])
# ensure all data is float 确保所有数据是浮动的
values = values.astype('float32')
# 归一化特征
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# 构建监督学习问题
# 指定滞后时间大小
n_hours = 8
n_features = 4
reframed = series_to_supervised(scaled,n_hours, 1)
# 丢弃我们并不想预测的列
#reframed.drop(reframed.columns[], axis=1, inplace=True)
print(reframed.head())

# %%     分割数据
values = reframed.values
n_train_hours = 365 * 24 * 3
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
# 分为输入和输出
n_obs = n_hours * n_features
train_X, train_y = train[:, :n_obs], train[:,-n_features:]
test_X, test_y = test[:, :n_obs], test[:, -n_features:]
print(train_X.shape, len(train_X), train_y.shape)
# 重塑为3D形状 [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# %%    学习
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# 设计网络
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(4))
model.compile(loss='mae', optimizer='adam')
# 拟合网络模型
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
#保存模型
model.save('air_analysis8h.model')
# 绘制历史数据
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

#%% 测试
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
# 加载模型
model = tf.keras.models.load_model('air_analysis8h.model')
test_X = test_X.reshape((test_X.shape[0], n_hours,n_features))
yhat = model.predict(test_X)
print(yhat[0])
#print(test_X[0,-1:])
# 反向转换预测值比例
#inv_yhat = concatenate((yhat, test_X[:,-1:]), axis=1)
inv_yhat = scaler.inverse_transform(yhat)
print(inv_yhat[0])
#inv_yhat = inv_yhat[:,0]
# 反向转换实际值大小
test_y = test_y.reshape((len(test_y), 4))
#inv_y = concatenate((test_y, test_X[:,-7:]), axis=1)
inv_y = scaler.inverse_transform(test_y)
print(inv_y[0])
#inv_y = inv_y[:,0]
# 计算RMSE大小
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)


# %% 实际值与预测值
pyplot.plot(inv_y, label='actual')
pyplot.plot(inv_yhat, label='prediction')
pyplot.legend()
pyplot.show()

# %%
numl=-10000
print(yhat[numl])
print(inv_yhat[numl])
print(test_y[numl])
print(inv_y[numl])
# %%
print(values[0])

# %%
