# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET 

# web_data = request.body.decode('utf-8')  use this to get data
# 这块应该 receive.py 来处理.   
def parse_xml(web_data):
    xmlData = ET.fromstring(web_data) 
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'voice':
        return VoiceMsg(xmlData)
    elif msg_type == 'video':
        return VideoMsg(xmlData)

class Msg(object):
    def __init__(self, xmlData):
        self.toUserName = xmlData.find('ToUserName').text
        self.fromUserName = xmlData.find('FromUserName').text
        self.createTime = xmlData.find('CreateTime').text
        self.msgType = xmlData.find('MsgType').text
        self.msgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.picUrl = xmlData.find('PicUrl').text
        self.mediaId = xmlData.find('MediaId').text

class VoiceMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.format = xmlData.find('Format').text
        self.recognition = xmlData.find('Recognition').text.encode("utf-8")
        self.mediaId = xmlData.find('MediaId').text

class VideoMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.mediaId = xmlData.find('MediaId').text
        self.thumbMediaId = xmlData.find('ThumbMediaId').text


