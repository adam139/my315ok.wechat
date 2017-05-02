#-*- coding: UTF-8 -*-

import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from my315ok.wechat.testing import FUNCTIONAL_TESTING 
from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest

from plone.namedfile.file import NamedImage
import os
from my315ok.wechat.tests.test_api import dummy_image

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
        item.image = dummy_image() 
        item.image_caption = "news image"        

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
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'type':'system',
                        'id': 'news1'}
        view = self.portal.restrictedTraverse('@@ajax_send_weixin')
        result = view()

        self.assertEqual(json.loads(result), {'info': 1})         

    def test_menu_create(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'id': 'news1'}
        view = self.portal['menufolder1'].restrictedTraverse('@@ajax_create_menu')
        result = view()

        self.assertEqual(json.loads(result), {'info': 0})
             
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        folder = portal['news1']


        page = folder.absolute_url() + '/@@send_as_wechat'
        browser.open(page)
        self.assertTrue('id="send"' in browser.contents)        
        
                      