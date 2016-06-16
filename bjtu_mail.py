# -*- encoding:utf-8 -*-
import cookielib
import urllib
import urllib2
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

hosturl = 'http://mail.bjtu.edu.cn/'
posturl = 'http://mail.bjtu.edu.cn/coremail/index.jsp?cus=1'
inbox= 'http://mail.bjtu.edu.cn/coremail/XJS/mbox/list.jsp?sid=EADMylGGsYahIcUYiiGGLgSzvFlFGytX&fid=1&nav_type=system'
cj = cookielib.LWPCookieJar()
urllib2.install_opener(urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler))

h = urllib2.urlopen(hosturl)

headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'''
}

postdata = {
    "locale": "zh_CN",
    "uid": "11274121",
    "nodetect": "false",
    "domain": "bjtu.edu.cn",
    "password": "sulixin1011slx",
    "action:login": ""
}

postdata = urllib.urlencode(postdata)
#print postdata

request = urllib2.Request(posturl, postdata, headers)
response = urllib2.urlopen(request)
text = response.read()
if u'收件箱' in text:
	print  u'登陆成功'
#print text


#response = urllib2.urlopen(inbox)
#text = response.read()
try:
  response = urllib2.urlopen(inbox)
  content = response.read()
except urllib2.HTTPError, e:
  if e.getcode() == 500:
    content = e.read()
  else:
    raise

print content
