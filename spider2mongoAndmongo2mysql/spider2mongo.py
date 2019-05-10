import requests
from bs4 import BeautifulSoup
import json
import pymongo


def get_soup_obj(url):
    url_obj = requests.get(url)
    soup = BeautifulSoup(url_obj.content, 'html.parser')
    return soup


def get_secondpage(city_aqi_item):
    """
    功能：
        通过二级网址获得城市的一些指数
    参数：
        city_aqi_item：二级网址
    返回值：
        通过城市对应的链接（二级网址）获得该城市的各种指数
    """

    info = []
    soup = get_soup_obj(city_aqi_item)
    data_div_tag = soup.find('div', class_='span12 data')
    value_div_tag_list = data_div_tag.find_all('div', class_='value')

    for value_div_tag in value_div_tag_list:
        info.append(value_div_tag.text)

    return info


def get_fistpage_and_secondpage(url, soup):
    """
    功能：
        通过一级网址获得城市名称和对应的链接（二级网址），然后通过对应的链接（二级网址）得到该城市的一些指数，
        这个方法可以通过传参二级网址调用get_secondpage方法获得城市对应的各种指数
    参数：
        url:一级网址
        soup:需要分析的一级网址的源代码数据
    返回值：
        返回一个列表，列表的元素是字典，字典的元素是城市名称、城市对应的链接、城市的各种指数
    """

    city_aqi_list = []

    top_div = soup.find('div', class_='hot')
    city_tag_list = top_div.find_all('li')

    for city_tag in city_tag_list:
        city_info = dict()
        city_info['city_name'] = city_tag.find('a').text
        city_link = url + city_tag.find('a')['href']
        city_info['city_link'] = city_link
        items = get_secondpage(city_link)
        city_info['AQI'] = float(items[0])
        city_info['PM25/1h'] = float(items[1])
        city_info['PM10/1h'] = float(items[2])
        city_info['CO/1h'] = float(items[3])
        city_info['NO2/1h'] = float(items[4])
        city_info['O3/1h'] = float(items[5])
        city_info['O3/8h'] = float(items[6])
        city_info['SO2/1h'] = float(items[7])

        city_aqi_list.append(city_info)

    return city_aqi_list


def write_city_aqi(city_aqi_data):
    file_path = './city_aqi.json'

    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(city_aqi_data, f, ensure_ascii=False)


if __name__ == "__main__":

    #     需要分析的url
    url = 'http://www.pm25.in/'

    #     获得url的解析数据
    soup = get_soup_obj(url)

    #     获得从一级网址和二级网址获得的结果数据综合
    city_aqi_list = get_fistpage_and_secondpage(url, soup)

    # 连接mongodb
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client.test  # test数据库
    cities = db.cities

    #     对爬取到的热门城市名称、城市链接、城市的各种指数数据进行遍历
    # for city_aqi in city_aqi_list:
    result = cities.insert(city_aqi_list)

    #     将得到的数据写入json文件
    #  write_city_aqi(city_aqi_list)
