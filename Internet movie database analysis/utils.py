# -*- coding: utf-8 -*-

"""
    文件名:    utils.py
    功能：     工具文件
"""
import pandas as pd


def inspect_data(df_data):
    """
        查看加载的数据基本信息
    """
    print('数据集基本信息：')
    print(df_data.info())
    
    print('数据集有{}行，{}列'.format(df_data.shape[0], df_data.shape[1]))
    print('数据预览:')
    print(df_data.head())


def process_missing_data(df_data, method='drop'):
    """
        处理缺失数据
    """
    if df_data.isnull().values.any():
        # 存在缺失数据
        if method == 'drop':
            df_data = df_data.dropna()    # 过滤nan
        elif method == 'fill':
            df_data = df_data.fillna(0.)  # 填充nan
    return df_data.reset_index(drop=True)


def analyse_gross(df_data, groupby_columns, csvfile_path):
    """
        分析票房数据并保存结果
        可尝试将该方法进行扩展，如analyze_imdb等
    """
    grouped_data = df_data.groupby(groupby_columns, as_index=False)['gross'].sum()
    sorted_grouped_data = grouped_data.sort_values(by='gross', ascending=False)
    sorted_grouped_data.to_csv(csvfile_path, index=False)
    

def get_genres_data(df_data):
    """
        重新构造基于电影类型的数据集
    """
    # 按类型分割列
    genre_df = df_data['genres'].str.split('|', expand=True)
    # 默认分割后的列名为 0, 1, ...
    # 设置新的列名
    n_cols = genre_df.shape[1]
    genre_cols = ['genre_{}'.format(i) for i in range(n_cols)]
    genre_df.columns = genre_cols

    # 合并data frame
    use_cols = ['movie_title'] + genre_cols
    concat_df = pd.concat([df_data, genre_df], axis=1)[use_cols].set_index('movie_title')
    stacked_df = concat_df.stack().to_frame()
    stacked_df.columns = ['genres']
    return stacked_df
