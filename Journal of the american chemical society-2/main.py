# -*- coding: utf-8 -*-

"""
    本项目的数据集是美国化学学会杂志从1996到2016的论文集,用以分析作者发表论文的情况。

    1 导入数据：获得作者的ID号列表和对应的论文数量
    2 分析论文的浏览次数：依据得到的作者的ID号列表，分析每个作者的论文被浏览次数，比如，浏览的总次数、浏览的平均次数、浏览的最多次数、浏览的最少次数
    3 分析发表论文的日期：依据作者的ID号列表，计算作者每年发表的论文次数，得到论文次数最多的年份，当论文次数最多的年份存在多个时，则保留最近的年份，同时，保留该年份对应的论文数量
    4 合并数据，存入文件：将作者ID号列表、论文数量、浏览次数、论文发表日期进行合并，将数据存入txt文件

"""

import sqlite3
import json
import datetime
import numpy as np


def connect_sqlite(sqlite_path):
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def get_papers_author_info(cur, author_paper_data):
    """
    功能：
        根据author_paper_data获得papers数据
    参数：
        author_paper_data包含作者的authorID号和论文数量
    返回值：
        将authorID作为键，authorID对应的papers数据作为值，以字典的形式返回数据
    """
    author_papers_dict = {}

    n = len(author_paper_data)
    for i in range(n):
        author_id = author_paper_data[i][0]
        paper_num = author_paper_data[i][1]

        paper_author_info = cur.execute(
            "select * from Papers as paper inner join Paper_Authors as paper_author on paper.paperID==paper_author.paperID \
            and paper_author.authorID='%d'" % author_id)
        author_papers_dict[author_id] = paper_author_info.fetchall()

        # 依据每个作者的author_id，判断得到的author_papers_dict[author_id]的论文数量和文件导入的论文数量是否相等，
        # 若是相等，则打印作者的ID号列表和论文数量,eg."authorID号是：5,论文数量paper_num是：30"，否则结束循环。

        if paper_num == len(author_papers_dict[author_id]):
            print("authorID号是：{},论文数量paper_num是：{}".format(author_id, paper_num))

    return author_papers_dict


def process_view_num(authors_id, author_papers_dict):
    """
    功能：
        根据authorID对每个作者的浏览次数进行求和，均值，最大值，最小值操作
    参数：
        authors_id：作者列表数据，包含作者的authorID号
        author_papers_dict：包含了每个作者的paper数据，键为authorID，值为paper数据
    返回值：
        sum_mean_max_min_view是一个二维数据结构，行数据是对浏览次数依次按照求和、均值、最大值、最小值的结果
    """
    sum_mean_max_min_view = []
    # 对authors_id进行遍历，根据authorID获得字典的值，即paper信息，然后使用"views"字段获得浏览次数，进而进行统计分析

    for anthor_id in authors_id:
        result_per_author = []
        for x in author_papers_dict[anthor_id]:
            result_per_author.append(x['views'])

        sum_mean_max_min_view.append(
            [sum(result_per_author), np.mean(result_per_author), max(result_per_author), min(result_per_author)])

    return sum_mean_max_min_view


def get_max_publishonline(year_num_dict):
    """
    功能：
        计算论文数量最多的年份，当年份存在多个时，则保留最近的年份和对应的论文数量
    参数：
        year_num_dict：{年份：论文数量}
    返回值：
        以列表形式返回论文的数量最多的最近年份和对应的论文数量
    """
    # 论文的最多数量
    max_year_num = 0
    # 论文数量最多的年份
    max_year = 0

    for value in year_num_dict.values():
        if value > max_year_num:
            max_year_num = value

    for key in year_num_dict.keys():
        if year_num_dict[key] == max_year_num:
            if key > max_year:
                max_year = key

    return [max_year, max_year_num]


def get_year_num_dict(year_pubonline):
    # 以字典形式返回作者每年发表的论文数量，year_num_dict = {年份：论文数量}
    year_num_only = np.unique(year_pubonline)
    year_num_dict = {}
    for year_num in year_num_only:
        year_num_dict[year_num] = year_pubonline.count(year_num)
    return year_num_dict


def get_publishonline_year(author_id, author_papers_dict):
    """
    功能：
        根据authorID，得到作者发表论文的年份
    参数：
        author_id：作者的authorID号
        author_papers_dict：包含了每个作者的paper数据，键为authorID，值为paper数据
    返回值：
        得到作者发表论文的年份列表
    """
    # 年份列表
    year_pubonline = []

    # 将发表日期进行数据转换，将得到的年份存储到年份列表中

    for info_paper in author_papers_dict[author_id]:
        date_str = info_paper['publishedOnline'].split(' ')[0]
        year_pubonline.append(datetime.datetime.strptime(date_str, '%Y-%m-%d').year)

    return get_year_num_dict(year_pubonline)


def main():
    """
        主函数
    """
    author_paper_data = []
    file_path = './dataFile/author_paper_data.json'

    with open(file_path) as f_obj:
        # 使用json模块导入之前保存的数据，得到数据的ID号和发表的论文数量，将最终结果存储在author_paper_data列表中

        information = json.load(f_obj)

    for info in information:
        author_paper_data.append([info['author_id'], info['papers_num']])

    authors_id, papers_num = zip(*author_paper_data)
    print("作者ID和发表论文数量为：")
    print(author_paper_data)
    print("=================================")

    conn, cur = connect_sqlite("./dataFile/database.sqlite")

    author_papers_dict = get_papers_author_info(cur, author_paper_data)

    views_lst = process_view_num(authors_id, author_papers_dict)
    print("=================================")
    print("发表论文超过20篇的作者的论文被浏览次数的和、均值、最大值、最小值依次为：")
    print(views_lst)

    year_num_lst = []
    for author_id in authors_id:
        year_num = get_publishonline_year(author_id, author_papers_dict)
        year_num_lst.append(get_max_publishonline(year_num))
    # year_num_lst是存储了年份和论文数量的列表
    # year_num_lst的每个元素是一个列表，这个列表为[publish_max_year,publish_year_num]，其中，第一个元素是authorID对应的论文数量最多的最近年份，第二个元素是论文的数量
    print("=================================")
    print("发表论文超过20篇的作者的论文数量最多的最近年份和该年份的论文数量分别为：")
    print(year_num_lst)

    # 合并数据，存入文件
    file_path = './dataFile/author_paper_data.txt'
    with open(file_path, 'w') as fn:

        # 根据authors_id列表的authorID号，将得到的数据列表author_paper_data(author_id,papers_num)、
        # views_lst(sum_view,mean_view,max_view,min_view)、year_num_lst(publish_max_year,publish_year_num)进行合并
        # 并且，将合并后的数据存入txt文件

        for i in range(len(authors_id)):
            nums = author_paper_data[i] + views_lst[i] + year_num_lst[i]
            a = ''
            for num in nums:
                a = a + ' ' + str(num)
            fn.write(a.lstrip() + '\n')

    # 关闭数据库
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
