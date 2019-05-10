# -*- coding: utf-8 -*-

"""
    全球食品数据分析

    任务：
        - 分析各国家食物中的食品添加剂种类个数

"""
import pandas as pd
import utils

# 数据文件地址
filename = './data/FoodFacts.csv'


def main():
    """
        主函数
    """
    # 读取数据
    data = pd.read_csv(filename, usecols=['countries_en', 'additives_n'])

    # 分析各国家食物中的食品添加剂种类个数
    # 1. 数据清洗
    # 去除缺失数据
    data = data.dropna()    # 或者data.dropna(inplace=True)

    # 2. 获取国家列表
    countries = utils.get_countries(data['countries_en'])

    # 3. 获取不同国家的食品添加剂的种类个数
    results_df = utils.get_additives_count(countries, data)

    # 4. 保存统计结果
    results_df.to_csv('./country_additives.csv', index=False)


if __name__ == '__main__':
    main()
