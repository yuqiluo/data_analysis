# -*- coding: utf-8 -*-

"""
    Lending Club借贷数据探索性分析及可视化

    任务：
        - 借贷金额分析可视化
        - 借贷目的占比可视化
        - 变量间关系可视化

"""

import pandas as pd
import matplotlib.pyplot as plt

import utils

# 设置显示的最多列数
pd.set_option('display.max_columns', 10)

# 解决matplotlib显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 使用的列
sel_cols = ['loan_amnt',    # 借贷金额
            'term',         # 借贷周期（单位：月）
            'annual_inc',   # 年收入
            'loan_status',  # 借贷状态
            'purpose',      # 借贷目的
            'addr_state',   # 所在的州
            ]

dataset_path = './dataset/loan.csv'


def main():
    """
        主函数
    """
    # 读取数据集
    raw_data = pd.read_csv(dataset_path, usecols=sel_cols)
    # 查看数据集
    utils.insepct_data(raw_data)

    # 处理数据集
    proc_data = utils.process_data(raw_data)

    # 借贷金额分析可视化
    utils.visualise_loan_amnt(proc_data, col_name='term', title='借贷周期vs借贷金额',
                              xlabel='借贷周期', save_path='./output/term_amnt.png')
    utils.visualise_loan_amnt(proc_data, col_name='loan_status', title='借贷状态vs借贷金额',
                              xlabel='借贷状态', save_path='./output/status_amnt.png')
    utils.visualise_loan_amnt(proc_data, col_name='purpose', title='借贷目的vs借贷金额',
                              xlabel='借贷目的', save_path='./output/purpose_amnt.png')
    utils.visualise_loan_amnt(proc_data, col_name='addr_state', title='州vs借贷金额',
                              xlabel='州', save_path='./output/state_amnt.png')

    # 借贷目的占比可视化
    utils.visualise_loan_purpose_percent(proc_data['purpose'], './output/purpose_percent.png')

    # 变量间关系可视化
    utils.visualise_relation(proc_data, './output/var_relation.png')


if __name__ == '__main__':
    main()
