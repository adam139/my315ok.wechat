#-*- coding: UTF-8 -*-
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

class TestProductsFolderView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

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
        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))        
        import transaction
        transaction.commit()
        folder = portal['menufolder1']
        
        page = folder.absolute_url() + '/@@view'
        browser.open(page)
        self.assertTrue('<div class="btn-group">' in browser.contents)
        page = folder.absolute_url() + '/@@send_as_wechat'
        browser.open(page)
        self.assertTrue('id="send"' in browser.contents)        
        
                      