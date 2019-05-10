# -*- coding: utf-8 -*-

"""
    文件名:    utils.py
    功能：     工具文件
"""
import matplotlib.pyplot as plt
import seaborn as sns


def insepct_data(df_data):
    """
        查看加载的数据基本信息
    """
    print('数据集基本信息：')
    print(df_data.info())

    print('数据集有{}行，{}列'.format(df_data.shape[0], df_data.shape[1]))
    print('数据预览:')
    print(df_data.head())


def process_data(raw_data):
    """
        处理原始数据集
    """
    # 去掉缺失值
    proc_data = raw_data.dropna()

    # 选择top 5 的借贷目的
    top_purposes = proc_data['purpose'].value_counts().head(5).index.tolist() #value_counts：统计所有非零元素的个数，默认以降序的方式输出Series

    # 将其余的purposes替换为other
    non_top_idx = proc_data[~proc_data['purpose'].isin(top_purposes)].index
    proc_data.loc[non_top_idx, 'purpose'] = 'other'

    return proc_data


def visualise_loan_amnt(df, col_name, title, xlabel, save_path):
    """
        借贷金额分析可视化
    """
    df.groupby(col_name)['loan_amnt'].mean().plot(kind='bar', title=title)
    plt.xlabel(xlabel)
    plt.ylabel('借贷金额（均值）')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def visualise_loan_purpose_percent(purpose_data, save_path):
    """
        可视化借贷目的比例
    """
    pur_count = purpose_data.value_counts()
    # pur_per = pur_count / len(pur_count)
    pur_count.plot(kind='pie', figsize=(6, 6), autopct='%.2f%%')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def visualise_relation(proc_data, save_path):
    """
        变量间关系可视化
    """
    sns.pairplot(proc_data, vars=['loan_amnt', 'annual_inc'], hue='purpose')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
