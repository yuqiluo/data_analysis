# -*- coding: utf-8 -*-

"""
    文件名:    utils.py
    功能：     工具文件
"""
import pandas as pd


def get_countries(countries_ser):
    """
        获取国家列表
    """
    # 1. 全部转换为小写
    proc_countries_ser = countries_ser.str.lower()

    # 2. 去掉包含','的数据，如：Albania,Belgium,France,Germany,Italy,Netherlands,Spain
    proc_countries_ser = proc_countries_ser[~proc_countries_ser.str.contains(',')]

    # 3. unique()获取数据的唯一值
    countries = proc_countries_ser.unique()

    print('共有{}个不同的国家'.format(len(countries)))

    return countries


def get_additives_count(countries, data):
    """
        获取每个国家的食品添加剂的种类个数
    """
    # 记录每个国家的统计值
    count_list = []

    # 1. 遍历国家，过滤对应的数据
    for country in countries:
        # countries是国家的小写，data中的数据没有处理，所以这里使用大小写不敏感的操作 case=False
        filtered_data = data[data['countries_en'].str.contains(country, case=False)]
        # 由于是不同时间点进行的记录，这里取均值作为统计
        count = filtered_data['additives_n'].mean()
        count_list.append(count)

    # 2. 构建DataFrame记录结果
    result_df = pd.DataFrame()
    result_df['country'] = countries
    result_df['count'] = count_list

    # 3. 按统计值排序
    result_df.sort_values('count', ascending=False, inplace=True)

    # 预览结果
    print('结果预览：')
    print(result_df.head())

    return result_df
