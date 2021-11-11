BOT_NAME = 'media'

SPIDER_MODULES = ['media.spiders']
NEWSPIDER_MODULE = 'media.spiders'
MEDIA_ALLOW_REDIRECTS = True
# ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'
# DOWNLOAD_DELAY = 10

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

ITEM_PIPELINES = {
   # 'media.pipelines.DuplicatesPipeline': 300,
   'media.pipelines.CsvPipeline': 301,
   # 'media.pipelines.MysqlPipeline': 302,
   # 'media.pipelines.MysqlCompany': 303,
}

KEYWORD_LIST = 'keyword_list.txt'

MEDIA_TYPE = '搜狐'

START_DATE = '2021-05-10'

END_DATE = '2021-05-12'




DOWNLOADER_MIDDLEWARES = {
   'media.middlewares.MediaDownloaderMiddleware': 543,
   # 'media.middlewares.ProxyMiddleware': 400,  #代理默认不开启
}

proxyUser = "代理用户名"
proxyPass = "代理密码"


MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'we_media'
