import cookielib
import urllib
import urllib2
import socket

hosturl = 'http://sep.ucas.ac.cn/'
posturl = 'http://sep.ucas.ac.cn/slogin'
courseurl = 'http://sep.ucas.ac.cn/portal/site/16'
cj = cookielib.LWPCookieJar()
urllib2.install_opener(urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler))

h = urllib2.urlopen(hosturl)

headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'''
}

postdata = {
    "userName": "sulixin15@mails.ucas.ac.cn",
    "pwd": "learnmore",
    "sb": "sb"
}

postdata = urllib.urlencode(postdata)
print postdata

request = urllib2.Request(posturl, postdata, headers)
response = urllib2.urlopen(request)
text = response.read()

print text


