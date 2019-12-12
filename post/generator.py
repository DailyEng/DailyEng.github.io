#!/usr/bin/python
#coding:utf-8
# encoding=utf8
import urllib, json
import sys
import httplib
import requests
import base64
reload(sys)
sys.setdefaultencoding('utf8')

url = "http://open.iciba.com/dsapi/" # http://open.iciba.com/dsapi/?date=2018-01-01
response = urllib.urlopen(url)
data = json.loads(response.read())

english = data['content']
chinese = data['note']
date = data['dateline']
pic_small = data['picture']
pic_big = data['picture2']
tags = '每日一句'
# dailyImg = 'https://source.unsplash.com/858x480/?' + chinese


filename = date + '.md'

# get random image then upload to Imgur, return image url
def dailyImg():
	url = "https://source.unsplash.com/858x480/?" + english
	response = requests.get(url)
	image = (base64.b64encode(response.content))
	return uploadImage(image)

# upload images to Imgur, return url
def uploadImage(imgUrl):
	url = "https://api.imgur.com/3/image"
	payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"image\"\r\n\r\n" + imgUrl + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
	headers = {
		'authorization': "Client-ID 3f4115cb3bc6a76",
		'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
		'Cache-Control': "no-cache",
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	data = json.loads(response.text)
	return data['data']['link']

# compress image with tinypng, return compressed url
def tiny(imgUrl):
	url = "https://api.tinify.com/shrink"
	payload = "{\n\t\"source\": {\n\t\t\"url\": \"" + imgUrl + "\"\n\t}\n}"
	headers = {
		'Authorization': "Basic YXBpOkRmRzVaVEFwVjRYem9vdm1tS1ZjVHlkT2tGLTk0RVVC",
		'Content-Type': "application/json",
		'Cache-Control': "no-cache",
	    }
	response = requests.request("POST", url, data=payload, headers=headers)
	data = json.loads(response.text)
	print 'Input Url: ' + imgUrl
	print 'TinyPNG: ' + data['output']['url']
	return data['output']['url']

# start md file
print 'Creating file ...'
file = open(filename, "w")
print 'Start writing ...'
file.write('---\n')
file.write('title: "' + chinese + '"\n')
file.write('date: ' + date + '\n')
file.write('tags: ["每日一句"]\n')
file.write('cover: "' + uploadImage(tiny(pic_small)) + '"\n')
file.write('---\n\n')

file.write('![' + chinese + '](' + uploadImage(tiny(pic_big)) + ')\n\n')

file.write('## 英文短句：\n> ' + english + '\n\n')
file.write('<!--more-->\n\n')
file.write('## 中文翻译：\n> ' + chinese + '\n\n')

file.write('![' + english + '](' + uploadImage(tiny(dailyImg())) + ')\n\n')
file.close()
print 'Done!'