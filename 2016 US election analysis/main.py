# -*- coding: utf-8 -*-

"""
    2016美国大选分析

    任务：
        - 分析每个月的民意调查统计趋势

"""

import utils

# 数据文件地址
filename = './presidential_polls.csv'


def main():
    """
        主函数
    """
    # 读取指定列的数据
    use_cols = ['enddate', 'rawpoll_clinton', 'rawpoll_trump']
    data_array = utils.load_data(filename, use_cols)

    # 处理日期格式数据，转换为yyyy-mm字符串
    proc_data_array = utils.process_date(data_array)

    # 统计每月的投票数据
    utils.get_month_stats(proc_data_array)


if __name__ == '__main__':
    main()
