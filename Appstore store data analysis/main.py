# -*- coding: utf-8 -*-

"""
    项目AppleStore数据集包含应用程序ID、名称、大小、价格、评分、内容评级、主要类型、支持设备类型数量等信息，共包括7207行

    字段的描述
    这个项目将对以下字段进行相关性分析。
    size_bytes： 大小（以字节为单位）
    price： 价格金额
    rating_count_tot： 用户评分计数（适用于所有版本）
    rating_count_ver：用户评分计数（当前版本）
    user_rating：平均用户评分值（适用于所有版本），取值范围为(0,5]，左开右闭区间
    user_rating_ver：平均用户评分值（对于当前版本）取值范围(0,5]，左开右闭区间
    prime_genre：主要类型
    sup_devices.num：支持设备的数量
    lang.num：支持的语言数量

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def drop_col(data_all, del_col):
    """
    功能：
        判断data_all数据集中是否存在del_col中的列，若是存在，则删除该列数据
    参数：
        data_all是DataFrame结构的数据集，del_col是一个列表，包含了要删除的列，需要inplace原数据集删除

    """
    data_all.drop(columns=del_col, inplace=True)


def drop_duplicat_row(data_all):
    """
    功能：
        原数据集删除重复行
    参数：
        data_all是DataFrame的数据集，也是本项目所用的数据集

    """
    data_all.drop_duplicates(inplace=True)


def drop_nan(data_all):
    """
    功能：
        原数据集删除缺失值
    参数：
        data_all是DataFrame的数据集，也是本项目所用的数据集

    """
    data_all.dropna(inplace=True)


def user_rating_group(ele):
    """
    功能：
        对用户评分user_rating的数据进行类别划分
    参数：
        ele是用户评分的每个元素
    返回值：
       返回类别,字符串类型数据
    """

    # 对用户评分user_rating进行类别划分，要求小于等于2.5的数值设定为'good'，大于等于4.5的设定为'best'，其他的设置为'better'
    if ele <= 2.5:
        ele_class = 'good'
    elif ele >= 4.5:
        ele_class = 'best'
    else:
        ele_class = 'better'

    return ele_class


def process(ele):
    """
    功能：
        依据用户评分类别user_rating_group，对'rating_count_ver'数据中的0值替换为组内均值
    参数：
        ele是'rating_count_ver'的一组元素
    返回值：
       对每组内的0值，使用组内均值来计算，且保留两位小数，然后返回修改后的数据。
    """

    # 对每组内的0值，使用组内均值来计算，且保留两位小数，然后返回修改后的数据
    ele_ser = ele.replace(0, ele.mean())

    return ele_ser


def a(s):
    b = s.split(' & ')
    return b[0]



def main():
    """
        主函数
    """
    filepath = './dataFile/AppleStore.csv'
    data_all = pd.read_csv(filepath, index_col=False)

    print('数据集中每列的信息：')
    print(data_all.info())

    print('==============================')
    print('前3行数据集为：')
    print(data_all.head(3))

    del_col = ['id', 'track_name', 'cont_rating', 'currency', 'ver', 'ipadSc_urls.num', 'vpp_lic']
    drop_col(data_all, del_col)

    # 打印data_all的列名和维度
    print('==============================')
    print('现在数据集data_all的列为：{}'.format(data_all.columns))
    print('现在数据集data_all的维度为：{}'.format(data_all.shape))

    print('==============================')
    print('去除重复行前，数据集的维度是：{}'.format(data_all.shape))
    drop_duplicat_row(data_all)
    print('去除重复行后，数据集的维度是：{}'.format(data_all.shape))

    drop_nan(data_all)

    print('==============================')
    print('处理完缺失值后，数据集的维度是：{}'.format(data_all.shape))

    print('==============================')
    print('数据集data_all每列数据的分布为：')
    print(data_all.describe())

    # 将列名为user_rating和user_rating_ver的列数据中所有大于5的数据设定为5。将列数据中评分为0的异常值设定为1.
    data_all['user_rating'].replace(0, 1, inplace=True)
    data_all['user_rating_ver'].replace(0, 1, inplace=True)
    user_rating_arr = data_all['user_rating'].values
    user_rating_arr[user_rating_arr > 5] = 5
    data_all['user_rating'] = user_rating_arr
    user_rating_ver_arr = data_all['user_rating_ver'].values
    user_rating_ver_arr[user_rating_ver_arr > 5] = 5
    data_all['user_rating_ver'] = user_rating_ver_arr
    # data_all['user_rating'][data_all['user_rating'] > 5] = 5
    # data_all['user_rating_ver'][data_all['user_rating_ver'] > 5] = 5

    data_all['user_rating_group'] = data_all['user_rating'].apply(user_rating_group)

    # 根据user_rating_group类别数据进行分组，然后对'rating_count_tot','rating_count_ver','user_rating','user_rating_ver'数据计算组内均值
    rating_data = data_all.groupby('user_rating_group')['rating_count_tot', 'rating_count_ver', 'user_rating', 'user_rating_ver'].mean()
    print('==============================')
    print('按user_rating_group分类后，rating_count_tot，rating_count_ver，user_rating，user_rating_ver的均值分别为：')
    print(rating_data)

    # 依据计算出来的rating_data数据，通过绘制2行2列的图，显示user_rating_group对应类别下各数据的走势。
    plt.figure(figsize=(12, 16))

    ax = plt.subplot(2, 2, 1)
    plt.plot([1, 2, 3], rating_data['rating_count_tot'])
    plt.xticks([1, 2, 3], ['best', 'better', 'good'])
    plt.title('rating_count_tot')

    plt.subplot(2, 2, 2, sharex=ax)
    plt.plot([1, 2, 3], rating_data['rating_count_ver'])
    plt.title('rating_count_ver')

    plt.subplot(2, 2, 3, sharex=ax)
    plt.plot([1, 2, 3], rating_data['user_rating'])
    plt.title('user_rating')

    plt.subplot(2, 2, 4, sharex=ax)
    plt.plot([1, 2, 3], rating_data['user_rating_ver'])
    plt.title('user_rating_ver')

    # plt.show()
    plt.savefig('./rating_data_mean.png')

    data_all['rating_count_data_new'] = data_all.groupby('user_rating_group')['rating_count_ver'].apply(process)

    # 根据类别数据user_rating_group，绘制关于'price', 'size_bytes', 'lang.num', 'sup_devices.num'的多变量图(pairplot)
    sns.pairplot(data=data_all, hue='user_rating_group', vars=['price', 'size_bytes', 'lang.num', 'sup_devices.num'], diag_kind='kde')

    # plt.show()
    plt.savefig('./pairplot.png')

    # 当app应用所属类型大于2个时，在所属类型prime_genre中，则多个类型之间以&进行类型连接
    # 现在我们仅需要保留多个类型中的第一个类型，将该类型作为该app所属类型
    # 最后将处理后的数据，以新的列数据保存在原数据集data_all中，列名为prime_genre_class，且将prime_genre列数据从原数据集中删除
    data_all['prime_genre_class'] = data_all['prime_genre'].apply(a)
    data_all.drop(columns=['prime_genre'])

    # 得到用户评级分较高的数据
    dataset = data_all[(data_all['user_rating_group'] == 'best')]

    # 使用透视表对size_bytes数据计算均值，其中行索引设置为prime_genre_class数据，列索引设置为sup_devices.num数据
    site_bytes_data = dataset.pivot_table(values='size_bytes', index='prime_genre_class', columns='sup_devices.num')

    plt.figure(figsize=(15, 10))
    plt.imshow(site_bytes_data, cmap=plt.cm.hot_r)
    plt.colorbar()
    plt.xticks(np.arange(site_bytes_data.shape[1]), np.sort(dataset['sup_devices.num'].unique()))
    plt.yticks(np.arange(site_bytes_data.shape[0]), np.sort(dataset['prime_genre_class'].unique()))
    plt.xlabel('sup_devices.num')
    plt.ylabel('prime_genre_class')
    plt.title('site_bytes_mean')

    # plt.show()
    plt.savefig('./site_bytes_mean.png')


if __name__ == '__main__':
    main()
