# coding=utf-8
import hashlib
from django.http import HttpResponse
from django.shortcuts import render
from wechat.models import BlogPost
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import urllib2,json
import time
import os
from lxml import etree

# Create your views here.

# make a fake blog post, so we should add data to model


def archive(request):
    posts = BlogPost.objects.all() #查询所有的 post, get data here.
    return render(request, 'archive.html', {'posts': posts}) # template hahaha

# you could change the template though
# all stuff about wechat is putted blow this line
# -------------

wechat_token = '12345678'

@csrf_exempt
def wechat(request):
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        # get all stuff we need from request

        token = wechat_token 
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        #encrypt sort it, hashlib it, then check the result

        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    elif request.method == "GET":
        # do something about POST here
        str_xml = request.body.decode('utf-8')    #use body to get raw data
        xml = etree.fromstring(str_xml)            
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text
        content = xml.find('Content').text   #获得用户所输入的内容
        msgId = xml.find('MsgId').text
        return render(request, 'reply_text.xml',
                      {'toUserName': fromUserName,
                       'fromUserName': toUserName,
                       'createTime': time.time(),
                       'msgType': msgType,
                       'content': content,
                       },
                       content_type = 'application/xml'
        )
