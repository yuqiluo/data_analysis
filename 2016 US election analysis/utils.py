# -*- coding: utf-8 -*-

"""
    文件名:    utils.py
    功能：     工具文件
"""
import numpy as np
import datetime
import pandas as pd


def load_data(filename, use_cols):
    """
        读取指定列的CSV数据
    """
    data_array = pd.read_csv(filename, usecols=use_cols).values.astype(str)
    return data_array


def process_date(data_array):
    """
        处理日期格式数据，转换为yyyy-mm字符串
    """
    enddate_lst = data_array[:, 0].tolist()

    # 将日期字符串格式统一，即'mm/dd/yy'
    enddate_lst = [enddate.replace('-', '/') for enddate in enddate_lst]

    # 将日期字符串转换成日期
    date_lst = [datetime.datetime.strptime(enddate, '%m/%d/%Y') for enddate in enddate_lst]

    # 构造年份-月份列表
    month_lst = ['{}-{:02d}'.format(date_obj.year, date_obj.month) for date_obj in date_lst]

    month_array = np.array(month_lst)

    data_array[:, 0] = month_array

    return data_array


def get_month_stats(data_array):
    """
        统计每月的投票数据
    """
    months = np.unique(data_array[:, 0])
    for month in months:
        # 根据月份过滤数据
        filtered_data = data_array[data_array[:, 0] == month]

        # 获取投票数据，字符串数组转换为数值型数组
        try:
            filtered_poll_data = filtered_data[:, 1:].astype(float)
        except ValueError:
            # 遇到不能转换为数值的字符串，跳过循环
            continue

        result = np.sum(filtered_poll_data, axis=0)

        # 在列方向求和
        print('{}，Clinton票数：{}，Trump票数：{}'.format(month, result[0], result[1]))
