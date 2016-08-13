#-*- coding: UTF-8 -*-

import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from my315ok.wechat.testing import FUNCTIONAL_TESTING 
from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager
from xml.etree import ElementTree
from my315ok.wechat.utilities import to_binary, to_text

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

class TestProductsFolderView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
#        portal.invokeFactory('collective.conference.conferencefolder','conferencefolder1')

        portal.invokeFactory('News Item','news1',
                                         title=u"news1",
                                         description=u"a news",
                                         text='news',

                                         )
        data = getFile('image.jpg').read()
        item = portal['news1']
        item.setImage(data, content_type="image/jpg")
        portal.invokeFactory('my315ok.wechat.content.menufolder', 'menufolder1',title="menufolder1")
        
        portal['menufolder1'].invokeFactory('my315ok.wechat.content.menu','menu1',
                                               title="xixi",
                                               menu_type="click",
                                               url="",
                                               istopmenu='1',
                                               key="rich text1")
        portal['menufolder1']['menu1'].invokeFactory('my315ok.wechat.content.menu','submenu1',
                                               title="submenu1-1",
                                               menu_type="click",
                                               url="",
                                               key="rich text1")
        portal['menufolder1']['menu1'].invokeFactory('my315ok.wechat.content.menu','submenu2',
                                               title="submenu1-2",
                                               menu_type="click",
                                               url="",
                                               key="rich text1")                
        portal['menufolder1'].invokeFactory('my315ok.wechat.content.menu','menu2',
                                               title="skip",
                                               menu_type="view",
                                               istopmenu="1",
                                               url="http://315ok.org/",
                                               key="rich text1")
        
        
        self.portal = portal
        
    def test_ajax_send(self):
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
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        #模拟微信服务器发来数据
        request.form = {
                        '_authenticator': auth,
                        'echostr':"ok",
                        'timestamp':'20141110',
                        'nonce':'2018',
                        'signature':'73ced4a61919b480adcc70f151e99f5edd5690c5',
                        'data': _make_xml("haha")}
        view = self.portal.restrictedTraverse('@@receive_weixin')
        result = view()
#        wechat_message = dict((child.tag, to_text(child.text)) for child in ElementTree.fromstring(result))
#        import pdb
#        pdb.set_trace()

#        self.assertEqual(wechat_message['MsgType'], u'news')         

                      