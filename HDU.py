# -*- coding：utf-8 -*-
'''
urllib——用于表单数据的生成
urllib2——必要的库，不再赘述
cookielib——提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源
re——用于正则表达式
HTMLParser——用于处理html代码的转义字符
'''
import urllib.request, urllib.error, urllib.parse
import re
import http.cookiejar
import string
import hashlib
import io
# 获取lt
def getLt():
	getLtURL = 'http://cas.hdu.edu.cn/cas/login?service=http://i.hdu.edu.cn/dcp/index.jsp'
	request = urllib.request.Request(getLtURL)
	response = urllib.request.urlopen(request)
	getLtContent = response.read().decode('utf-8')
	getLt = re.search(r'value="(LT-.*?)"',getLtContent)
	return getLt.group(1)
#输入账号密码
username = input("请输入学号")
password = input("请输入密码")

targetURL = 'http://cas.hdu.edu.cn/cas/login?service=http://i.hdu.edu.cn/dcp/index.jsp'
values = {'username': username,
          'password': hashlib.md5(password.encode('utf-8')).hexdigest(),# 进行md5加密,hashlib.md5（data）函数，数据参数的类型应该是'bytes'。
          'lt':getLt()
         }
data = urllib.parse.urlencode(values).encode('utf-8')

cookie = http.cookiejar.MozillaCookieJar('cookie.txt')
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')]

response = opener.open(urllib.request.Request(targetURL, data)).read().decode('gbk','ignore')
ST = re.search(r'ticket=(.*?)"', response).group(1)
opener.open('http://i.hdu.edu.cn/dcp/index.jsp?ticket='+ ST)
opener.open('http://i.hdu.edu.cn/dcp/forward.action?path=/portal/portal&p=wkHomePage')
get_response = opener.open('http://cas.hdu.edu.cn/cas/login?service=http://jxgl.hdu.edu.cn/index.aspx')
the_page = get_response.read().decode('gbk')
getST = re.search(r'ticket=(.*?)"', the_page)
ST = getST.group(1)
opener.open('http://jxgl.hdu.edu.cn/index.aspx?ticket='+ ST)
target = opener.open('http://jxgl.hdu.edu.cn/xs_main.aspx?xh='+ username).read().decode('gbk')
getTarget = re.search(r'<a href="xsxk.aspx\?xh=(.*?)&xm=(.*?)&gnmkdm=(.*?)".*?>成绩查询<', target)
get_url = 'http://jxgl.hdu.edu.cn/xscjcx_dq.aspx?xh=%s&xm=%s&gnmkdm=%s'%(getTarget.group(1),urllib.parse.quote(getTarget.group(2)),getTarget.group(3)) # 利用cookie请求访问另一个网址
values = {'ddlxn': '',
          'ddlxq': '',
          '__EVENTTARGET':'',
          '__EVENTARGUMENT':'',
          '__LASTFOCUS':'',
          '__VIEWSTATE':'/wEPDwULLTIxMDUwNTQwMjIPZBYCAgEPZBYGAgEPEGQQFRIACTIwMDEtMjAwMgkyMDAyLTIwMDMJMjAwMy0yMDA0CTIwMDQtMjAwNQkyMDA1LTIwMDYJMjAwNi0yMDA3CTIwMDctMjAwOAkyMDA4LTIwMDkJMjAwOS0yMDEwCTIwMTAtMjAxMQkyMDExLTIwMTIJMjAxMi0yMDEzCTIwMTMtMjAxNAkyMDE0LTIwMTUJMjAxNS0yMDE2CTIwMTYtMjAxNwkyMDE3LTIwMTgVEgAJMjAwMS0yMDAyCTIwMDItMjAwMwkyMDAzLTIwMDQJMjAwNC0yMDA1CTIwMDUtMjAwNgkyMDA2LTIwMDcJMjAwNy0yMDA4CTIwMDgtMjAwOQkyMDA5LTIwMTAJMjAxMC0yMDExCTIwMTEtMjAxMgkyMDEyLTIwMTMJMjAxMy0yMDE0CTIwMTQtMjAxNQkyMDE1LTIwMTYJMjAxNi0yMDE3CTIwMTctMjAxOBQrAxJnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZAIHD2QWBmYPZBYCZg8WAh4JaW5uZXJodG1sBSUyMDE3LTIwMTjlrablubTnrKwx5a2m5pyf5a2m5Lmg5oiQ57upZAIBD2QWBmYPFgIfAAUR5a2m5Y+377yaMTQxMDg0MTlkAgEPFgIfAAUS5aeT5ZCN77ya5bq35a6H6LGqZAICDxYCHwAFGOWtpumZou+8muiuoeeul+acuuWtpumZomQCAg9kFgRmDxYCHwAFFeS4k+S4mu+8mui9r+S7tuW3peeoi2QCAQ8WAh8ABRTooYzmlL/nj63vvJoxNDEwODQxNGQCCQ88KwALAQAPFggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50Zh4JUGFnZUNvdW50AgEeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudGZkZGQ=',
          '__EVENTVALIDATION':'/wEWGQLO+Y7JCQKOwemfDgKOwemfDgKc6PHxDgKf6O1nApbomfIPApnotegBApjoofIMApvo3egOApLoyfINApXopYsNAprozbADAsCqyt4FAsOqjp8DAsKqkt8CAt2q1h8C3Kq63wMC36r+nwEC3qrCXwLZqobgAQL/wOmfDgL/wOmfDgLwr8PxAgLxr8PxAgLwksmiDg==',
          'btnCx':'',
         }
data = urllib.parse.urlencode(values).encode('utf-8')
opener.addheaders = [('Referer', 'http://jxgl.hdu.edu.cn/cas/login')] #重定向问题用Referer解决
get_request = urllib.request.Request(get_url, data)
get_response = opener.open(get_request)
target = get_response.read().decode('gbk', 'ignore')
num_data = re.compile('<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>').findall(target)
with open("credit.data", "w", encoding='utf-8') as data:
	for a in num_data[1:]:
		if a[8] == '&nbsp;':
			data.write(a[0] + ' ' +a[1]+ ' ' +a[2] + ' ' + a[3] + ' ' + a[4] + ' '+a[6] + ' ' + a[7] + ' ' + a[10]+'\n')
		elif int(a[8])>60:
			data.write(a[0] + ' ' +a[1]+ ' ' +a[2] + ' ' + a[3] + ' ' + a[4] + ' '+a[6] + ' ' + a[8] + ' ' + a[10]+'\n')

data.close()
cookie.save(ignore_discard=True, ignore_expires=True)

