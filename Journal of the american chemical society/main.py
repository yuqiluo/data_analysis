# -*- coding: utf-8 -*-

"""
    本项目的数据集是美国化学学会杂志从1996到2016的论文集,用以分析作者发表论文的情况。

    数据集中包括三个表：

    Authors：对作者进行描述
    Paper_Authors：对作者发表论文的情况进行描述
    Papers：关于论文的表

"""

import sqlite3
import json
import numpy as np


def connect_sqlite(sqlite_path):

    conn = sqlite3.connect(sqlite_path)

    # 将conn.row_factory设置为sqlite3.Row,这个设置很重要，不然不能通过字段名获得数据，下面row的代码需要放在conn代码之后，cur的代码之前
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    return conn, cur


def get_authorid_and_papernum(cur, authors):
    """
    功能：
        计算论文数量大于20的作者，得到该作者的authorID和论文数量
    参数：
        authors是Authors表的每一行数据
    返回值：
        以列表的形式返回authorID和论文数量
    """
    paper_authors = []

    # 将authorID和论文数量用paper_authors列表存放，paer_authors的格式如 paper_authors = [[1,56],[2,23]],表示authorID==1的作者，
    # 发表了56个论文，authorID==2的作者，发表了23个论文

    for author in authors:
        cur.execute('select paperID from Paper_Authors where authorID = {};'.format(author['authorID']))
        data = cur.fetchall()
        if len(data) > 20:
            paper_authors.append([author['authorID'], len(data)])

    return paper_authors


def get_author_name(cur, author_id):
    """
    功能：
        根据authorID，从Authors表中得到forename和surname字段，进而得到作者的名字
    参数：
        cur是游标，author_id是作者的authorID号
    返回值：
        返回作者的名字,字符串类型
    """

    # 使用单空格将Authors表中的forename和surname字段进行拼接，返回作者的名字
    name_lst = cur.execute('select forename, surname from Authors where authorID = {};'.format(author_id)).fetchall()
    for name_list in name_lst:
        name = name_list[0] + ' ' + name_list[1]

    return name


def main():
    """
        主函数
    """
    conn, cur = connect_sqlite("./dataFile/database.sqlite")

    # 打印数据库中的所有表的名字，此处通过字段名来获得数据
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_data = cur.fetchall()
    print("数据库中所有表的名称为：")
    for table_d in table_data:
        print(table_d['name'])

    print("====================================")
    # 调用游标的description方法，获得Authors表的字段名
    cur.execute("select * from Authors")
    col_name_list = [tuple[0] for tuple in cur.description]
    print("Authors表的字段名为：", col_name_list)

    print("====================================")
    # 执行PRAGMA table_info语句获取Authors表结构信息，并且打印
    print("Authors表的结构信息为：")
    cur.execute("PRAGMA table_info({})".format('Authors'))
    for author in cur.fetchall():
        print([author[i] for i in range(len(author))])

    print("====================================")
    # 获得Authors表中authorID的个数及非重复个数，其中，使用np.unique，可以计算非重复个数
    cur.execute("select * from Authors")
    author_data = cur.fetchall()
    authors = [author['authorID'] for author in author_data]  # 在数据库那设置了row之后，就可以通过字段名来获取列数据了
    authors_all = len(authors)
    authors_only = len(np.unique(authors))
    print("Authors表中authorID的个数为：{}个".format(authors_all))
    print("去重后，Authors表中authorID的个数为：{}个".format(authors_only))

    print("====================================")
    # 获得Papers表的信息
    cur.execute("select * from Papers")
    name_paper_lst = [tuple[0] for tuple in cur.description]
    print("Papers表的字段名为：", name_paper_lst)

    print("====================================")
    print("以下是Papers表中paperID，publishedOnline，views字段的前10行数据\n")
    cur.execute("select * from Papers")
    data_papers = cur.fetchmany(10)
    for data_paper in data_papers:
        print(data_paper['paperID'], data_paper['publishedOnline'], data_paper['views'])

    print("====================================")
    # 获得Papers表中paperID的个数及非重复个数
    cur.execute("select * from Papers")
    papers = [paper['paperID'] for paper in cur.fetchall()]
    paper_all = len(papers)
    paper_only = len(np.unique(papers))
    print("Papers表中paperID的个数为：{}个".format(paper_all))
    print("去重后，Papers表中paperID的个数为：{}个".format(paper_only))

    print("====================================")
    # 查看Paper_Authors表包含的字段
    cur.execute("select * from Paper_Authors")
    col_name_list = [tuple[0] for tuple in cur.description]
    print("Paper_Authors表的字段名为：", col_name_list)

    print("====================================")
    print("以下是Paper_Authors表中authorID，paperID字段的前20行数据\n")
    cur.execute("select * from Paper_Authors limit 20")
    datas = cur.fetchall()
    for data in datas:
        print(data['authorID'], data['paperID'])

    print("====================================")
    # 分析Authors、Papers、Paper_Authors表的数据量存在的隐含关系
    cur.execute("select * from Paper_Authors")
    paper_author_data = cur.fetchall()
    paper_author_authorid = [paper_author["authorID"] for paper_author in paper_author_data]
    print("Paper_Authors表包括: {}条数据".format(len(paper_author_authorid)))
    print("Paper_Authors表包括: {}条唯一的authorID数据".format(len(np.unique(paper_author_authorid))))

    print("====================================")
    paper_author_paperid = [paper_author["paperID"] for paper_author in paper_author_data]
    print("Paper_Authors表包括: {}条数据".format(len(paper_author_paperid)))
    print("Paper_Authors表包括: {}条唯一的paperID数据".format(len(np.unique(paper_author_paperid))))

    print("====================================")
    # 由于Authors的数据较多，因此，这里仅获得前100名author的authorID，对前100名作者的论文情况进行分析
    authors = cur.execute("select * from Authors limit 100").fetchall()
    authorid_papernum_lst = get_authorid_and_papernum(cur, authors)
    print("论文数量大于20的作者的authorID和论文数量为：")
    print(authorid_papernum_lst)

    print("====================================")
    # 从以上得到的结果authorid_papernum_lst列表中得到作者的ID号列表
    authors_id = []
    for authorid_papernum in authorid_papernum_lst:
        authors_id.append(authorid_papernum[0])
    print("作者的ID号列表中的authorID号为：{},作者列表包含{}个作者的ID号".format(authors_id, len(authors_id)))

    print("====================================")
    # authors_name_lst是作者的名字列表，该列表包括20个名字
    authors_name_lst = [get_author_name(cur, author_id) for author_id in authors_id]
    print("作者的名字列表为：{}".format(authors_name_lst))

    # 合并数据
    total_author_paper_lst = []
    for i in range(len(authors_id)):
        # 按照authorID的ID号，将得到的数据列表author_name_lst(authors_name)、authorid_papernum_lst(author_id,papers_num)依次赋值给
        # 名称为"author_name","author_id","papers_num"的数据结构（字典），最后将结果存入total_author_paper_lst中

        author_paper = dict()

        author_paper['author_name:'] = authors_name_lst[i]
        author_paper['author_id:'] = authorid_papernum_lst[i][0]
        author_paper['papers_num:'] = authorid_papernum_lst[i][1]

        total_author_paper_lst.append(author_paper)

    # 存入文件
    file_path = './dataFile/author_paper_data.json'
    # 将数据total_author_paper_lst存入author_paper_data.json文件

    with open(file_path, mode='w') as f_obj:
        json.dump(total_author_paper_lst, f_obj)

    # 关闭数据库
    conn.commit()

    conn.close()


if __name__ == '__main__':
    main()
