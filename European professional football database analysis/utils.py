# -*- coding: utf-8 -*-

"""
    文件名:    utils.py
    功能：     工具文件
"""
import datetime


def get_age(birthday_str):
    """
        根据生日获取年龄
    """
    born_year = int(birthday_str.split('-')[0])  # '1989-12-15 00:00:00' -> 1989
    current_year = datetime.datetime.now().date().year
    return current_year - born_year


def get_overall_rating(cur, player_api_id):
    """
        获取球员平均评分
    """
    rows = cur.execute("SELECT overall_rating FROM Player_Attributes \
                             WHERE player_api_id = {};".format(player_api_id)).fetchall()
    ratings = [float(row[0])
               for row in rows
               if row[0] is not None]
    mean_rating = sum(ratings) / len(ratings)
    return mean_rating
