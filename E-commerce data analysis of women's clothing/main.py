# -*- coding: utf-8 -*-

"""
    女性服装电子商务数据分析

"""
import numpy as np
import pandas as pd


def get_alldata(filename):
    """
    功能：
        通过文件的路径，得到所有数据，然后根据给定的列名，得到索引，再根据索引获得对应的数据集 ，数据集的每一行都是一个客户的评论
    参数：
        文件的路径：womens_clothing_e-commerce_reviews.csv
    返回值：
        返回给定列的所有数据，以array的形式返回

    """
    col_names = ['Clothing ID', 'Recommended IND', 'Positive Feedback Count', 'Class Name']
    dataset = pd.read_csv(filename, usecols=col_names).values.astype(str)

    return dataset


def get_id_count_arr(dataset):
    """
    功能：
        由于数据集的每一行都是一个客户的评论，因此这个函数根据Clothing ID来分析对应的评论数，
    参数：
        "Clothing ID,Recommended IND,Positive Feedback Count,Class Name"列的所有数据集，数据集的每一行都是一个客户的评论
    返回值：
        返回评论大于400的所有Clothing ID号
    """

    # 计算每个Clothing ID的评论数，将Clothing ID的数量大于400的数据放入id_count_lst中

    id_count_lst = []
    clothing_ids = dataset[:, 0].tolist()
    for clothing_id in np.unique(clothing_ids).tolist():
        if clothing_ids.count(clothing_id) > 400:
            id_count_lst.append(clothing_id)

    return id_count_lst


def cal_recom_num(dataset, id_lst):
    """
    功能：
        计算每个Clothing ID代表的服装被评论的次数列表，以及被推荐的次数列表
    参数：
        dataset：需要被分析的数据集
        id_lst：需要被分析的唯一Clothing ID号
    返回值：
        id_recom_ratio_lst：返回推荐次数占评论次数的比例，即得到这个Clothing ID代表的服装的受欢迎程度
    """

    # 元素为被推荐次数占评论数的比例
    id_recom_ratio_lst = []

    # dataset的每列的列名依次为"服装号(Clothing ID),推荐标识(Recommended IND),积极反馈（Positive Feedback Count）,服装类型（Class Name）"，
    # 故被推荐次数的索引为1，该列中的数据只有0和1，1表示推荐，0表示不推荐
    # 现在需要通过id_lst和dataset，利用数组的性质，计算每个Clothing ID号代表服装的被推荐的比例，即推荐次数比上评论次数

    for id_ in id_lst:
        comment_times = dataset[:, 0].tolist().count(id_)
        filtered_data = dataset[dataset[:, 0] == id_]
        recom_times = filtered_data[:, 1].tolist().count('1')

        id_recom_ratio_lst.append(recom_times / comment_times)

    return id_recom_ratio_lst


def cal_pos_num(dataset, id_lst):
    """
    功能：
        Positive Feedback Count列是每个评论被赞同的次数，计算每个Clothing ID的评论被赞同的总次数。
    参数：
        dataset：需要被分析的数据集
        id_lst：需要被分析的唯一Clothing ID号

    返回值：
        id_pos_sum_lst中的元素为每个Clothing ID的评论被赞同的和（总次数）。
        id_name_lst中的每个元素是Clothing ID的服装类型。
    """
    # 每个Clothing ID进行正反馈次数加和的列表
    id_pos_sum_lst = []
    # 每个Clothing ID的类型名称
    id_name_lst = []

    # dataset的每列的列名依次为"服装号(Clothing ID),推荐标识(Recommended IND),积极反馈（Positive Feedback Count）,服装类型（Class Name）"，
    # 对每个Clothing ID被评论的正反馈次数进行加和统计和对应的服装类型Class Name

    for id_ in id_lst:
        filtered_data = dataset[dataset[:, 0] == id_]
        pos_feedback = filtered_data[:, 2].astype(int)
        total = np.sum(pos_feedback)
        class_name = filtered_data[0, 3]
        id_pos_sum_lst.append(total)
        id_name_lst.append(class_name)

    return id_pos_sum_lst, id_name_lst


def main():
    """
        主函数
    """
    filename = "./dataFile/womens_clothing_e-commerce_reviews.csv"
    dataset = get_alldata(filename)
    print("数据集dataset的维度是: {}".format(dataset.shape))
    print("================================")

    # 计算评论次数大于400的唯一Clothing ID号
    id_count_lst = get_id_count_arr(dataset)
    print("评论次数大于400的唯一Clothing ID号有{}个，列表是{}".format(len(id_count_lst), id_count_lst))
    print("================================")

    recom_ratio_lst = cal_recom_num(dataset, id_count_lst)

    # 对每个Clothing ID的服装被评论的积极反馈进行数量统计
    id_pos_sum_lst, id_name_lst = cal_pos_num(dataset, id_count_lst)

    # 将id_count_lst，id_count_lst,id_data_lst,id_recom_lst,id_pos_sum_arr进行合并
    id_data_arrs = np.array((id_count_lst, id_name_lst, recom_ratio_lst, id_pos_sum_lst)).T
    for id_data in id_data_arrs:
        print(
            "Clothing ID为 {} ,服装类型为 {},被推荐的占比为: {}，正反馈的总计数为: {}".format(id_data[0], id_data[1], id_data[2], id_data[3]))


if __name__ == '__main__':
    main()
