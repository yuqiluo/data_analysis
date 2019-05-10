from pymongo import MongoClient
import pymysql


class Mongo2Mysql(object):
    def enable_mysql(self, mysql_host, mysql_port, database, username, password, charset):
        """
        启动连接mysql数据库
        :return: conn链接对象,mysql_cs游标对象
        """
        try:
            conn = pymysql.connect(
                host=mysql_host,
                port=mysql_port,
                database=database,
                user=username,
                password=password,
                charset=charset,
            )
            mysql_cs = conn.cursor()
            return conn, mysql_cs
        except Exception as e:
            print('mysql连接异常')
            raise e

    def enable_mongo(self, mongo_host, mongo_port, db_name, collection):
        """
        开启mongo的链接
        :param db_name: 要链接的数据库名称,字符串
        :param collection: 数据库内集合名称,字符串
        :return: coll 集合对象
        """
        try:
            client = MongoClient(host=mongo_host, port=mongo_port)  # 只有这里会报错
            coll = client[db_name][collection]  # 获取数据集合
            return coll
        except Exception as e:
            print('mongodb连接异常')
            raise e

    def data_from_mongo(self, item, *args):
        """
        从mongodb取出数据
        :*args: 需要获取的字段key,字符串
        :return: 列表,需要取出的数据,这个列表将作为构造sql语句时的params参数
        """
        params = list()
        for key in args:
            params.append(item.get(key))
        return params

    def set_sql(self, tb_name, params: list):
        """构造sql语句,暂时先自行在外设置,后续完善"""
        # TODO
        pass

    def insert(self, mysql_cs, conn, sql, params):
        """执行插入语句"""
        try:
            mysql_cs.execute(sql, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e


def main():
    m2s = Mongo2Mysql()
    # 连接mongodb
    coll = m2s.enable_mongo('localhost', 27017, 'test', 'cities')
    # 连接mysql,得到游标对象和连接对象
    conn, mysql_cs = m2s.enable_mysql('localhost', 3306, 'test', 'root', 'lyq984358', 'utf8')
    # 从mongodb中查询出数据的游标对象,可以自定义查询结果
    data_cursor = coll.find({})
    # 构造需要从mongodb中得到的字段名称列表
    args = ['city_name', 'city_link', 'AQI', 'PM25/1h', 'PM10/1h', 'CO/1h', 'NO2/1h', 'O3/1h', 'O3/8h', 'SO2/1h']
    # 遍历cursor对象获取每一条记录
    for item in data_cursor:
        # 从mongodb中得到每条记录的真实数据,用来构造sql语句中的values
        params = m2s.data_from_mongo(item, *args)
        print(params)
        # TODO sql带参数的语句,自行指定哪些字段需要被插入数据,默认情况下,mysql字段名和args相同
        sql = 'insert into aqi_city (city_name,city_link,AQI,PM25_1h,PM10_1h,CO_1h,NO2_1h,O3_1h,O3_8h,SO2_1h) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # 执行插入
        m2s.insert(mysql_cs, conn, sql, params)
    # 关闭连接
    mysql_cs.close()
    conn.close()
    print('数据插入完成')


if __name__ == '__main__':
    main()








