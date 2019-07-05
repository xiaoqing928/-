# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 20:53
# @Author  : xiaoqing
# @File    : data.py
# @Software: PyCharm Community Edition

import pandas as pd

df = pd.read_csv('F:/Subway/Metro_train/record_2019-01-01.csv')
df.head(5)

'''
题目说了每十分钟为一个单位，这里先对时间做一下处理
'''
df['day'] = df['time'].apply(lambda x: int(x[8:10]))
df['week'] = pd.to_datetime(df['time']).dt.dayofweek + 1
df['weekend'] = (pd.to_datetime(df.time).dt.weekday >= 5).astype(int)
df.head(5)

# 时间处理
def process_time(df):
    # 获取第几天
    df['day'] = df['time'].apply(lambda x: int(x[8:10]))
    # 获取周几
    df['week'] = pd.to_datetime(df['time']).dt.dayofweek + 1
    # 是否是周末
    df['weekend'] = (pd.to_datetime(df.time).dt.weekday >= 5).astype(int)
    # 获取小时数
    df['hour'] = df['time'].apply(lambda x: int(x[11:13]))
    # 获取分钟数
    df['minute'] = df['time'].apply(lambda x: int(x[14:15] + '0'))
    # 删除time列
    del df['time']
    return df

df = process_time(df)
df.head(5)

'''
    每个站点每条线每周每天每小时每十分钟的数量
'''
# df.groupby(['stationID','week', 'lineID','weekend', 'day', 'hour', 'minute'])['status'].count().reset_index()
# df.groupby(['stationID','week', 'lineID','weekend', 'day', 'hour', 'minute'])['status'].sum().reset_index()

result = df.groupby(['stationID','week', 'lineID','weekend', 'day', 'hour', 'minute'])['status'].aggregate(['count', 'sum']).reset_index()

result['inNums'] = result['sum']
result['outNums'] = result['count'] - result['sum']

result['day_since_first'] = result['day'] - 1


'''
    处理基本的特征
'''
def get_base_features(df):
    # count,sum
    result = df.groupby(['stationID', 'week', 'lineID', 'weekend', 'day', 'hour', 'minute'])['status'].aggregate(
        ['count', 'sum']).reset_index()

    # 各个站每10分钟一段的流量情况
    result['inNums'] = result['sum']
    result['outNums'] = result['count'] - result['sum']

    result['day_since_first'] = result['day'] - 1
    result.fillna(0, inplace=True)

    del result['sum'], result['count']
    return result
r = get_base_features(df)
r.columns

import os

path = 'F:/Subway/Metro_train/'
#加载所有文件数据

data_list = os.listdir(path)
for i in range(0, len(data_list)):
    if data_list[i].split('.')[-1] == 'csv':
        print('已加载',data_list[i], i)
        df = pd.read_csv(path + data_list[i])
        df = process_time(df)
        df = get_base_features(df)
        r = pd.concat([r, df], axis=0, ignore_index=True)
    else:
        continue
print(r.head(5))
# data_list = os.listdir(path)
# for filename in data_list:
#     if filename.split('.')[1] == 'csv':
#         print('已加载：', filename)
#         df = pd.read_csv(path + filename)
#         df = process_time(df)
#         df = get_base_features(df)
#         data = pd.concat([data, df], axis=0, ignore_index=True)
