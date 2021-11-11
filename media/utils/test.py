from datetime import datetime,timedelta
from fake_useragent import UserAgent
# print(UserAgent().random)
import time
import os
import sys
import media.utils.util as util

import requests



# 要访问的目标页面
targetUrl = "http://test.abuyun.com"
# targetUrl = "http://proxy.abuyun.com/switch-ip"
# targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HH4GX42N2E901O9D"
proxyPass = "1272FE89D8437162"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
print(proxyMeta)


proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)

print(resp.status_code)

print(resp.text)





# exit()


# gpc = "stf=1617206400,1619020800|stftype=1"
# page = 0
#
#
# base_url = 'https://www.baidu.com/s?q1={}&gpc={}&q6={}&rn=50&pn='.format('艾格', gpc, 'sohu.com')
# url = base_url + str(page)

