# -*- coding: utf-8 -*-

"""
    欧洲职业足球数据库分析

    任务：
        - 根据数据库中球员的信息获取每个球员的姓名、年龄、体重、身高和平均得分

"""

import sqlite3
import json

import utils


# 声明变量
db_filepath = './database/soccer.db'    # 数据库文件路径
json_filepath = './player.json'     # 保存的球员JSON文件


def get_players_info(cur, n_players=None):
    """
        多表查询获取球员基本数据
    """
    # 从Player表中获取球员基本信息
    if n_players:
        # 获取指定个数的球员信息
        sql = "SELECT * FROM Player LIMIT {};".format(n_players)
    else:
        # 获取所有球员信息
        sql = "SELECT * FROM Player;"

    rows = cur.execute(sql).fetchall()

    # 构造球员列表
    player_list = []
    for row in rows:
        player = dict()
        # 1. 姓名
        player['name'] = row[2]
        # 2. 年龄
        birthday_str = row[4]
        player['age'] = utils.get_age(birthday_str)
        # 3. 体重
        player['weight'] = row[5]
        # 4. 身高
        player['height'] = row[6]
        # 5. 平均评分
        player_api_id = row[1]
        player['average rating'] = utils.get_overall_rating(cur, player_api_id)

        player_list.append(player)

    # 将处理后的结果保存到JSON文件中
    with open(json_filepath, 'w') as f:
        json.dump(player_list, f)


def main():
    """
        主函数
    """
    # 连接数据库
    conn = sqlite3.connect(db_filepath)
    cursor = conn.cursor()

    # 获取球员基本信息
    get_players_info(cursor, n_players=50)

    # 分析结束，关闭数据库
    conn.close()

    
if __name__ == '__main__':
    main()

