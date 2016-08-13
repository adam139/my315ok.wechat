# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.wechat.testing import FUNCTIONAL_TESTING 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest

from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')
import time
from my315ok.wechat.parser import parse_user_msg
from my315ok.wechat.reply import TextReply

class TestProductsFolderView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    
    def test_render_text_reply(self):
        message = parse_user_msg("""
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>
    """)
        t = int(time.time())
        reply = TextReply(message=message, content="aa", time=t)
        reply.render().strip() == """
    <xml>
    <ToUserName><![CDATA[fromUser]]></ToUserName>
    <FromUserName><![CDATA[toUser]]></FromUserName>
    <CreateTime>{time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[aa]]></Content>
    <FuncFlag>0</FuncFlag>
    </xml>""".format(time=t).strip()
