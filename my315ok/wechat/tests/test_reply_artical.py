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
import hashlib
import time
import six

#from nose.tools import raises
from my315ok.wechat.receive import BaseRoBot
from my315ok.wechat.utilities import generate_token, to_text

from my315ok.wechat.reply import create_reply,ArticlesReply,WeChatReply,Article

class TestProductsFolderView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def test_signature_checker(self):
        token = generate_token()
        robot = BaseRoBot(token)
        timestamp = str(int(time.time()))
        nonce = '12345678'

        sign = [token, timestamp, nonce]
        sign.sort()
        sign = ''.join(sign)
        if six.PY3:
            sign = sign.encode()
        sign = hashlib.sha1(sign).hexdigest()
        assert robot.check_signature(timestamp, nonce, sign)
        
    def test_replay_artical(self):
        import re
        import my315ok.wechat.testing
        robot = BaseRoBot()
        def _make_xml(content):
            return """
            <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>1348831860</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <MsgId>1234567890123456</MsgId>
            </xml>
        """ % content
        
        @robot.text
        def echo(message):
            import pdb
            pdb.set_trace()
            a1 = ArticlesReply(message=message,star=True,MsgType="news",ArticleCount=1)
            item = Article(title=u"Plone技术论坛",img="",description="最大的中文Plone技术社区",url="http://plone.315ok.org/")
            a1.add_article(item)
            return a1   

        tester = my315ok.wechat.testing.WeTest(robot)   
        replyobj = tester.send_xml(_make_xml("啊"))
        create_reply(replyobj)
