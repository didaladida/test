# -*- encoding:utf-8 -*-
import cookielib
import urllib
import urllib2
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

hosturl = 'http://www.jooxn.com/Login.aspx'
posturl = 'http://www.jooxn.com/Login.aspx'
redirected = 'http://www.jooxn.com/'
cj = cookielib.LWPCookieJar()
urllib2.install_opener(urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler))

h = urllib2.urlopen(hosturl)
content = h.read().decode('gbk')
# print  content
# id="__VIEWSTATEGENERATOR" value="2DB93210"
regular = {
    'viewstate': re.compile(r'id="__VIEWSTATE" value="(.+)" />'),
    'viewstatgenerator': re.compile(r'id="__VIEWSTATEGENERATOR" value="(.+)" />')
}
VIEWSTATE = regular['viewstate'].findall(content)[0]
VIEWSTATEGENERATOR = regular['viewstatgenerator'].findall(content)[0]
print VIEWSTATE
print VIEWSTATEGENERATOR
headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'''
}

postdata = {
    "__VIEWSTATE": VIEWSTATE,
    "tbUser": "ytyyy",
    "tbPassword": "123456",
    "tbValidCode": "1364",
    "btnLogin": u" 登 录 ".encode('gb2312'),
    "mac": "",
    "zt": "",
    "hfSubmit": "login",
    "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR
}

postdata = urllib.urlencode(postdata)

request = urllib2.Request(posturl, postdata, headers)
response = urllib2.urlopen(request)
text = response.read().decode('gbk')
print text

url1 = 'http://www.jooxn.com/Menus.aspx'
response = urllib2.urlopen(url1)
text=response.read().decode('gbk')
#print text
