import unittest
import transaction
from datetime import datetime
from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from my315ok.wechat.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from my315ok.wechat.interfaces import IwechatSettings

class TestSetup(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    

    
    def test_setting_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        self.assertEqual(settings.appid, "wx77d2f3625808f911")
        self.assertEqual(settings.redirecturi, "http://www.xtcs.org/")

        self.assertEqual(settings.access_token_time, datetime.strptime("2014-08-14 00:00:00", '%Y-%m-%d %H:%M:%S'))



class TestControlPanel(unittest.TestCase):

    layer = FUNCTIONAL_TESTING


    def test_render_plone_page(self):
        
        app = self.layer['app']
        portal = self.layer['portal']        
        transaction.commit()        
        browser = Browser(app)   
        browser.open(portal.absolute_url() + "/@@my315okwechat-controlpanel")
        self.assertTrue('<aside id="global_statusmessage">' in browser.contents)
