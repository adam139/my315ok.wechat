import unittest
from zope import event
from my315ok.wechat.testing import INTEGRATION_TESTING
from my315ok.wechat.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility


from Products.ATContentTypes.content.newsitem import ATNewsItem
from my315ok.wechat.events import SendWechatEvent


from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from my315ok.wechat.tests.test_api import setupbase

class TestEvent(setupbase):
    
    layer = INTEGRATION_TESTING
    
    def test_sendwechat_event(self):
        item = self.portal['news1']
        
        event.notify(SendWechatEvent(item))
        
         

       
class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING