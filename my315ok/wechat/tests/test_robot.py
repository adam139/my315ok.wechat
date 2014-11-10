# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.wechat.testing import FUNCTIONAL_TESTING 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest

from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')
import hashlib
import time
import six


from my315ok.wechat.receive import BaseRoBot as WeRoBot
from my315ok.wechat.utilities import generate_token, to_text

from my315ok.wechat.reply import create_reply,ArticlesReply,WeChatReply
class TestProductsFolderView(unittest.TestCase):
    
    def test_signature_checker(self):
        token = generate_token()

        robot = WeRoBot(token)

        timestamp = str(int(time.time()))
        nonce = '12345678'

        sign = [token, timestamp, nonce]
        sign.sort()
        sign = ''.join(sign)
        if six.PY3:
            sign = sign.encode()
        sign = hashlib.sha1(sign).hexdigest()

        assert robot.check_signature(timestamp, nonce, sign)


    def test_register_handlers(self):
        robot = WeRoBot()

        for type in robot.message_types:
            assert hasattr(robot, type)

        @robot.text
        def text_handler():
            return "Hi"

        assert robot._handlers["text"] == [(text_handler, 0)]

        @robot.image
        def image_handler(message):
            return 'nice pic'

        assert robot._handlers["image"] == [(image_handler, 1)]

        assert robot.get_handlers("text") == [(text_handler, 0)]

        @robot.handler
        def handler(message, session):
            pass

        assert robot.get_handlers("text") == [(text_handler, 0), (handler, 2)]

        @robot.location
        def location_handler():
            pass

        assert robot._handlers["location"] == [(location_handler, 0)]


        @robot.link
        def link_handler():
            pass
    
        assert robot._handlers["link"] == [(link_handler, 0)]

        @robot.subscribe
        def subscribe_handler():
            pass

        assert robot._handlers["subscribe"] == [(subscribe_handler, 0)]

        @robot.unsubscribe
        def unsubscribe_handler():
            pass

        assert robot._handlers["unsubscribe"] == [(unsubscribe_handler, 0)]

        @robot.voice
        def voice_handler():
            pass

        assert robot._handlers["voice"] == [(voice_handler, 0)]

        @robot.click
        def click_handler():
            pass

        assert robot._handlers["click"] == [(click_handler, 0)]

        @robot.key_click("MENU")
        def menu_handler():
            pass

        assert len(robot._handlers["click"]) == 2


    def test_filter(self):
        import re
        import my315ok.wechat.testing
        robot = WeRoBot()


        @robot.filter("喵")
        def _():
            return "喵"

        assert len(robot._handlers["text"]) == 1

        @robot.filter(re.compile(to_text(".*?呵呵.*?")))
        def _():
            return "哼"

        assert len(robot._handlers["text"]) == 2

        @robot.text
        def _():
            return "汪"

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

        tester = my315ok.wechat.testing.WeTest(robot)

        assert tester.send_xml(_make_xml("啊")) == "汪"
   
        assert to_text(tester.send_xml(_make_xml("啊呵呵了"))) == to_text("哼")
        assert tester.send_xml(_make_xml("喵")) == "喵"

        robot = WeRoBot()

        @robot.filter("帮助", "跪求帮助", re.compile(".*?help.*?"))
        def _():
            return "就不帮"

        assert len(robot._handlers["text"]) == 3

        @robot.text
        def _():
            return "哦"
    
#        @robot.text
#        def echo(message):
#            ArticlesReply(message=message,star=True,\
#                      MsgType="news",ArticleCount=1,Title=u"Plone技术论坛",\
#                      Decsription="最大的中文Plone技术社区",Url="http://plone.315ok.org/"
#                      )
#            return ArticlesReply    

        tester = my315ok.wechat.testing.WeTest(robot)

        assert tester.send_xml(_make_xml("啊")) == "哦"
        assert tester.send_xml(_make_xml("帮助")) == "就不帮"
        assert tester.send_xml(_make_xml("跪求帮助")) == "就不帮"  
        assert tester.send_xml(_make_xml("ooohelp")) == "就不帮"



