#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.wechat.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING 
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
    
    layer = INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('my315ok.wechat.content.messagefolder', 'messagefolder1',title="messagefolder1")
        
        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.textmessage','textmessage',
                                               Content="xixi",
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn")        


        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.imagemessage','imagemessage',
                                               MediaId="12345",
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn",
                                               PicUrl="http://315ok.org/")
         
        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.linkmessage','linkmessage',
                                               title="link message",
                                               description="link message",
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn",
                                               Url="http://315ok.org/") 
        
        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.voicemessage','voicemessage',
                                               MediaId="12345",
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn",
                                               Format="amr")
         
        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.videomessage','videomessage',
                                               MediaId="12345",
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn",
                                               ThumbMediaId="789")
                         
        portal['messagefolder1'].invokeFactory('my315ok.wechat.content.locationmessage','locationmessage',
                                               Location_X=12.5,
                                               Location_y=23.4,
                                               Scale=20,
                                               MsgType="text",
                                               FromUserName="plone",
                                               MsgId='123',
                                               ToUserName="plonecn",
                                               Label="xt location") 


        self.portal = portal
                
    def test_marketfolder(self):
        self.assertEqual(self.portal['messagefolder1'].id,'messagefolder1')
        self.assertEqual(self.portal['messagefolder1']['textmessage'].id,'textmessage')        
        self.assertEqual(self.portal['messagefolder1']['imagemessage'].id,'imagemessage')     
        self.assertEqual(self.portal['messagefolder1']['linkmessage'].id,'linkmessage')
        self.assertEqual(self.portal['messagefolder1']['voicemessage'].id,'voicemessage')
        self.assertEqual(self.portal['messagefolder1']['videomessage'].id,'videomessage')
        self.assertEqual(self.portal['messagefolder1']['locationmessage'].id,'locationmessage')                                
                      