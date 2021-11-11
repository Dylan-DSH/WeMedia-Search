
import sys
import time




def get_list(file_name):
    with open(file_name,'rb') as f :
        try:
            lines = f.read().splitlines()
            lines = [line.decode('utf-8-sig') for line in lines]
        except UnicodeDecodeError:
            print(u'%s文件应为utf-8编码，请先将文件转成utf-8在运行程序',file_name)
            sys.exit()
        word_list = []
        for line in lines:
            if line:
                word_list.append(line)
    return word_list


def convert_media_type(media_type):
    if media_type == "人民号":
        object_url = "rmh.pdnews.cn"

    elif media_type == "网易":
        media_info = {'object_url':'dy.163.com',
                      'redis_key':'wangyi_uid',
                      }

    elif media_type == "搜狐":
        media_info = {'object_url':'sohu.com',
                      'redis_key':'sohu_uid',
                      }

    elif media_type == "百家号":
        media_info = {'object_url':'baijiahao.baidu.com',
                      'redis_key':'baijiahao_uid',
                      }

    elif media_type == "澎湃新闻":
        object_url = "www.thepaper.cn"
    return media_info

def date_to_stamp(date, flag=0):
    datechar = (date + ' 00:00:00') if not flag else date + ' 23:59:59'
    stampchar = time.strptime(datechar,"%Y-%m-%d %H:%M:%S")
    stamp = str(int(time.mktime(stampchar)))
    return stamp