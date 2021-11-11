import sys
import os
import re
from datetime import datetime,timedelta
import media.utils.util as util


import scrapy
from scrapy.utils.project import get_project_settings
from media.items import MediaItem


class SearchSpider(scrapy.Spider):
    name = 'search'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']

    settings = get_project_settings()
    keyword_list = settings.get('KEYWORD_LIST')
    if not isinstance(keyword_list,list):
        if not os.path.isabs(keyword_list):
            keyword_list = os.getcwd() + os.sep+ 'media\\utils\\' +'keyword_list.txt'
            # print(keyword_list)
        if not os.path.isfile(keyword_list):
            sys.exit('不存在%s文件'%keyword_list)
        keyword_list = util.get_list(keyword_list)

    media_type = settings.get('MEDIA_TYPE')
    media_info = util.convert_media_type(media_type)
    media_url = media_info['object_url']

    start_data = settings.get('START_DATE')
    end_data = settings.get('END_DATE')
    mongo_erro = False
    pymongo_erro = False
    mysql_erro = False
    pymysql_erro = False


    def start_requests(self):
        start_time = util.date_to_stamp(self.start_data)
        end_time = util.date_to_stamp(self.end_data)
        gpc = "stf={},{}|stftype=1".format(start_time,end_time)
        page = 0

        for keyword in self.keyword_list:
            base_url = 'https://www.baidu.com/s?q1={}&gpc={}&q6={}&rn=50&pn={}'.format(keyword,gpc,self.media_url,'{}')
            url = base_url.format(str(page))
            print(url)
            yield scrapy.Request(url=url,
                                 # dont_filter=True,
                                 callback=self.parse_model,
                                 meta={
                                     'base_url':base_url,
                                     'page':page,
                                     'keyword':keyword
                                 })



    def parse_model(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']

        div_list = response.xpath('//div[@id="content_left"]/div')
        for div in div_list:
            href = div.xpath('./h3/a/@href')
            if href:
                news_url = href.extract_first()
                yield scrapy.Request(url=news_url,
                                     callback=self.parse_detail,
                                     meta={'keyword':keyword})

        if '下一页' in response.text:
            print("="*30+"现在的页数是："+str(page)+"="*30)
            base_url = response.meta['base_url']
            page  = page + 50
            url = base_url.format(str(page))
            yield scrapy.Request(url=url,
                                 callback=self.parse_model,
                                 meta={
                                     'base_url':base_url,
                                     'page':page,
                                     'keyword':keyword
                                 })


    def parse_detail(self, response):
        d_url = response.url
        content = response.text
        keyword = response.meta['keyword']
        media = MediaItem()

        if self.media_type == '搜狐':
            try:
                findUrl = re.compile(r'(www.sohu.com/n?a/\d+_\d+)')
                Url = re.findall(findUrl,content)
                if len(Url) == 0:
                    Url = re.findall(r'(www.sohu.com/n?a/\d+_\d+)',d_url)
                wemedia_url = "https://" + Url[0]
                wemedia_id = wemedia_url.split('_')[1]
                name = re.findall(r'name="mediaid" content="(.*?)"', content)[0]
                media['wemedia_name'] = name
                media['wemedia_id'] = wemedia_id
                media['wemedia_url'] = wemedia_url
                media['website_id'] = 23
                media['auth_level'] = 0
                media['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(name, wemedia_id)
                yield {'media': media,'keyword': keyword,'media_type': self.media_type}

            except Exception as e:
                pass



        elif self.media_type == '网易':
            try:
                if 'dy/media/T' in d_url:
                    name = re.findall(r'<h1 class="media_name">(.*?)</h1>',content)[0]
                    wemedia_url = d_url
                    wemedia_id = wemedia_url.split('/')[-1]
                    wemedia_id = wemedia_id.split('.')[0]

                else:
                    findName = re.compile(r'"https?://www.163.com/dy/media/T\d+?.html">(.*?)</a>')
                    findUrl = re.compile(r'"(https?://www.163.com/dy/media/T\d+?.html)">.*?</a>')
                    name = re.findall(findName,content)[0]
                    wemedia_url = re.findall(findUrl,content)[0]
                    wemedia_id = wemedia_url.split('/')[-1]
                    wemedia_id = wemedia_id.split('.')[0]

                media['wemedia_name'] = name
                media['wemedia_id'] = wemedia_id
                media['wemedia_url'] = wemedia_url
                media['website_id'] = 23
                media['auth_level'] = 0
                media['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(name, wemedia_id)
                yield {'media': media, 'keyword': keyword,'media_type': self.media_type}
            except Exception as e:
                print(e)
