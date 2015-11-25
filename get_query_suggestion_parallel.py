#encoding=gbk
import multiprocessing as mp
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError  
import json
import sys
import random
import time
import cookielib
import re
import os

reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_random_proxy_ip(proxy_ip):
	return random.choice(proxy_ip)
def get_sogou_query_suggestion( index, querys ):
	global proxy_ip
	global result_path

	if not os.path.isdir(result_path+"/suggestion_sogou"):
		os.mkdir(result_path+"/suggestion_sogou") 
	suggestion_filename=result_path+"/suggestion_sogou/"+str(index)
	suggestion_file=file(suggestion_filename, "w")
		
	j=0
	for i in range(len(querys)):
		if i % 10 != index:	
			continue
		if j % 100 == 0:
			random_proxy_ip=get_random_proxy_ip(proxy_ip)
			print "random_proxy_ip", random_proxy_ip
			#添加cookie
			__cookie = cookielib.CookieJar()
			cookie=urllib2.HTTPCookieProcessor(__cookie)
			__req = urllib2.build_opener(cookie)
			urllib2.install_opener(__req)
			urllib2.urlopen('https://www.sogou.com/')

			proxy = urllib2.ProxyHandler({'http': random_proxy_ip })
			opener = urllib2.build_opener(proxy)

		query=querys[i]
		query=query.replace(" ", "%20")
		url="https://www.sogou.com/suggnew/ajajjson?key="+ query+"&type=web&ori=yes&pr=web&abtestid=2&ipn="
#		print "url", url
		#有些词会失败
		try:
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
		except Exception as  e:
			print e.reason
			j+=1
			suggestion_file.write(query+"\t"+"ERROR"+"\n")
			continue
		html=response.read()
		stripped_html=html[17:-5] #去掉头尾无用字符
#		print "stripped_html", stripped_html
		if stripped_html == "":
			print "query, stripped_html", stripped_html, query
			j+=1
		else:
			json_html=json.loads(stripped_html.decode('gbk').encode('utf-8'))

			suggestion=""
			for suggest in json_html[1]:
				if suggestion == "":
					suggestion=suggest.decode('utf-8').encode('gbk') #去掉头尾的引号
				else:
					suggestion+=("\t"+suggest.decode('utf-8').encode('gbk'))
#			print "suggestion", suggestion	
			query=query.replace("%20", " ") #再替换回来
			suggestion_file.write(query+"\t"+suggestion+"\n")
			j+=1

	suggestion_file.close()

#百度也是用utf-8编码
def get_baidu_query_suggestion(index ,querys):
	global proxy_ip

	if not os.path.isdir(result_path+"/suggestion_baidu"):
		os.mkdir(result_path+"/suggestion_baidu") 
	suggestion_filename=result_path+"/suggestion_baidu/"+str(index)
	suggestion_file=file(suggestion_filename, "w")
	j=0
	for i in range(len(querys)):
		if i % 10 != index:	
			continue
		if j % 100 == 0:
			random_proxy_ip=get_random_proxy_ip(proxy_ip)
			print "random_proxy_ip", random_proxy_ip
			#添加cookie
			__cookie = cookielib.CookieJar()
			cookie=urllib2.HTTPCookieProcessor(__cookie)
			__req = urllib2.build_opener(cookie)
			urllib2.install_opener(__req)
			urllib2.urlopen('http://www.baidu.com/')

			proxy = urllib2.ProxyHandler({'http': random_proxy_ip })
			opener = urllib2.build_opener(proxy)
#		url="http://suggestion.baidu.com/su?wd="+query  # 
		query=querys[i]
		query=query.replace(" ", "%20")
		url="https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd="+query
		try:
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
			request = urllib2.Request(url.decode('gbk').encode('utf-8'), headers=headers)
			response = urllib2.urlopen(request)
		except Exception as e:
			suggestion_file.write(query+"\t"+"ERROR"+"\n")
			j+=1
			continue

		html=response.read()
		stripped_html=html[17:-2] #去掉头尾无用字符

		if len(stripped_html) == 20:
			print "query, stripped_html", stripped_html, query
			suggestion_file.write(query+"\n")
			j+=1
			continue
		else:
			splitted=stripped_html.split("[") #用[分隔，最后两个字符无用
			splitted2=splitted[1][:-2].split(",")
			suggestion=""
			for k in range(len(splitted2)):
				if k == 0:
					suggestion=splitted2[k][1:-1] #去掉头尾的引号
				else:
					suggestion+=("\t"+splitted2[k][1:-1])
			
			query=query.replace("%20", " ") #再替换回来
			suggestion_file.write(query+"\t"+suggestion+"\n")
			j+=1

	suggestion_file.close()

#360也是用utf-8编码
def get_360_query_suggestion(index, querys):
	global proxy_ip

	if not os.path.isdir(result_path+"/suggestion_360"):
		os.mkdir(result_path+"/suggestion_360") 
	suggestion_filename=result_path+"/suggestion_360/"+str(index)
	suggestion_file=file(suggestion_filename, "w")
	j=0
	for i in range(len(querys)):	
		if i % 10 != index:	
			continue
		if j % 100 == 0:
			random_proxy_ip=get_random_proxy_ip(proxy_ip)
			print "random_proxy_ip", random_proxy_ip

			#添加cookie
			__cookie = cookielib.CookieJar()
			cookie=urllib2.HTTPCookieProcessor(__cookie)
			__req = urllib2.build_opener(cookie)
			urllib2.install_opener(__req)
	#			urllib2.urlopen('http://www.so.360.cn/')

			proxy = urllib2.ProxyHandler({'http': random_proxy_ip })
			opener = urllib2.build_opener(proxy)

		query=querys[i]
		query=query.replace(" ", "%20") #有些引擎无法正确处理带空格的关键词
		url="http://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word,obdata&word="+query
		try:
			headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
			request = urllib2.Request(url.decode('gbk').encode('utf-8'), headers=headers)
			response = urllib2.urlopen(request)
		except Exception as e:
			suggestion_file.write(query+"\t"+"ERROR"+"\n")
			j+=1
			continue

		html=response.read()
		stripped_html=html[12:-2] #去掉头尾无用字符

	#	if stripped_html == "":
	#		print "query, stripped_html", stripped_html, query
	#		j+=1
	#	else:
		#把反斜杠进行转义，因为json无法处理反斜杠
		regex = re.compile(r'\\(?![/u"])')
		fixed_html = regex.sub(r"\\\\", stripped_html)

		try:
			json_html=json.loads(fixed_html)
		except  Exception as e:
			print "fixed_html", fixed_html
			j+=1
			continue

		suggestion=""
		for kv in json_html["result"]:
			for key, value in kv.items():
				if key=="word":
					if suggestion == "":
						suggestion=value.decode('utf-8').encode('gbk')
					else:
						suggestion+=("\t"+value.decode('utf-8').encode('gbk'))
					
		query=query.replace("%20", " ") #再替换回来
		suggestion_file.write(query+"\t"+suggestion+"\n")
		j+=1
	suggestion_file.close()	
def read_proxy_ip(proxy_ip):
	proxy_ip_file=file(proxy_ip,"r")
	proxy_ip_list=[]
	for line in proxy_ip_file:
		proxy_ip_list.append(line.strip())
	
	return proxy_ip_list

if __name__=='__main__':
	proxy_ip=read_proxy_ip("proxy_ip")
	engine_name=sys.argv[1]
	query_filename=sys.argv[2]
	result_path=sys.argv[3]
	query_file=file(query_filename, "r")
	i=0
	querys=[]
	for line in query_file:
		i+=1
		query=line.strip()
		querys.append(query)
		if i %1000 == 0:
			print i

	#pool = mul.Pool()
	#print mul.cpu_count()
	start=time.time()
	if engine_name=="sogou":
		processes = [mp.Process(target=get_sogou_query_suggestion, args=(i, querys)) for i in range(10) ]
	elif engine_name=="baidu":
		processes = [mp.Process(target=get_baidu_query_suggestion, args=(i, querys)) for i in range(10) ]
	else:
		processes = [mp.Process(target=get_360_query_suggestion, args=(i, querys)) for i in range(10) ]
	for p in processes:
		p.start()

	# Exit the completed processes
	for p in processes:
		p.join()

	end=time.time()
	print "it takes %f sec" % (end-start)
