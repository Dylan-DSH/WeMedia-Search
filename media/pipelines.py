import os
import csv
from redis import Redis
import media.utils.util as util

import scrapy
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from scrapy.exceptions import DropItem


class CsvPipeline(object):
    def process_item(self, item, spider):
        base_dir = '结果文件' + os.sep + settings.get('MEDIA_TYPE')
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep +settings.get('END_DATE') + '.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if item:
            with open(file_path,'a',encoding='utf-8-sig',newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = ['wemedia_name','wemedia_id','wemedia_url','site_id','auth_level','create_time']
                    writer.writerow(header)
                writer.writerow(
                    [item['media'][key] for key in item['media'].keys()]
                )
        return item

class MysqlPipeline(object):
    def create_database(self,mysql_config):
        """创建mysql数据库"""
        import pymysql
        sql = """CREATE DATABASE IF NOT EXISTS %s DEFAULT 
        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """% settings.get('MYSQL_DATABASE','we_media')
        db = pymysql.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()

    def create_table(self):
        """创建Mysql表"""
        sql = """
            CREATE TABLE IF NOT EXISTS media_account(
            id int(10) unsigned NOT NULL AUTO_INCREMENT ,
            media_type varchar (30) NOT NULL ,
            user_name varchar(30) ,
            user_id varchar(20) NOT NULL ,
            user_url varchar(100) NOT NULL ,
            submission_data datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.cursor.execute(sql)

    def open_spider(self,spider):
        try:
            import pymysql
            mysql_config = {
                'host':settings.get('MYSQL_HOST','localhost'),
                'port':settings.get('MYSQL_PORT',3306),
                'user':settings.get('MYSQL_USER','root'),
                'password':settings.get('MYSQL_PASSWORD','123456'),
                'charset':'utf8mb4'
            }
            self.create_database(mysql_config)
            mysql_config['db'] = settings.get('MYSQL_DATABASE','we_media')
            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError:
            spider.pysql_error = True

    def process_item(self,item,spider):
        data = dict(item['media'])
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table='wemedia_account_info_guohao',keys=keys,values=values)
        try:
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        return item

    def close_spider(self,spider):
        try:
            self.db.close()
        except Exception:
            pass

class MysqlCompany(object):
    db = ''
    cursor = ''

    def open_spider(self,spider):
        try:
            import pymysql
            mysql_config = {
                'host':settings.get('MYSQL_HOST','localhost'),
                'port':settings.get('MYSQL_PORT',3306),
                'user':settings.get('MYSQL_USER','root'),
                'password':settings.get('MYSQL_PASSWORD','123456'),
                'charset':'utf8mb4',
                'db':'we_media'
            }


            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError:
            spider.pysql_error = True

    def process_item(self,item,spider):
        data = dict(item['media'])

        keys = ', '.join(data.keys())
        print(keys)
        values = ', '.join(['%s'] * len(data))
        print(values)
        sql = """INSERT INTO {table}({keys}) VALUES ({values})""".format(table='wemedia_account_info_guohao',keys=keys,values=values)
        try:
            print(tuple(data.values()))
            self.cursor.execute(sql,tuple(data.values()))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        return item

    def close_spider(self,spider):
        try:
            self.db.close()
        except Exception:
            pass

class DuplicatesPipeline(object):
    def __init__(self):
        self.conn = Redis(host='127.0.0.1',port=6379)
        media_type = settings.get('MEDIA_TYPE')
        media_info = util.convert_media_type(media_type)
        self.redis_key = media_info['redis_key']


    def process_item(self, item, spider):
        uid = item['media']['wemedia_id']
        ex = self.conn.sadd(self.redis_key,uid)
        if ex == 1:
            return item
        else:
            raise DropItem('过滤重复的自媒体：%s' % item)
