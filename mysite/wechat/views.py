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
import receive
import reply


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
    
    elif request.method == "POST":
        str_xml = request.body.decode('utf-8')    #use body to get raw data          
        recMsg = receive.parse_xml(str_xml) # 注意要引用 receive.py
        toUserName = recMsg.toUserName
        fromUserName = recMsg.fromUserName

        if recMsg.msgType == 'text':
            cool = "You send me a stupid message: "
            msgType = recMsg.msgType
            createTime = recMsg.createTime
            content = cool + recMsg.content
            # 2. 以下是尝试的新玩法
            replyMsg = reply.TextMsg(fromUserName, toUserName, content)
            return HttpResponse(replyMsg.send())
 
''' 1. 已经成功的玩法
            return render(request, 'reply_text.xml',
                          {'toUserName': fromUserName,
                           'fromUserName': toUserName,
                           'createTime': createTime,
                           'msgType': msgType,
                           'content': content,
                           },
                            content_type = 'application/xml'
        )
        '''

 