import unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from my315ok.wechat.testing import FUNCTIONAL_TESTING

class TestControlPanel(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def test_navigate_save(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        from my315ok.wechat.interfaces import IwechatSettings
        
        app = self.layer['app']
        portal = self.layer['portal']
        
        browser = Browser(app)
        browser.handleErrors = False
        
        # Simulate HTTP Basic authentication
        browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )
        
        # Open Plone's site setup
        browser.open("%s/plone_control_panel" % portal.absolute_url())
        
        # Go to the control panel
        browser.getLink('Wechat settings').click()
        
        # Edit the appid  field
        browser.getControl(name='form.widgets.appid').value = "32"
        browser.getControl('Save').click()
        
        # Verify that this made it into the registry
        registry = getUtility(IRegistry)
        import pdb
        pdb.set_trace()
        settings = registry.forInterface(IwechatSettings)
        self.assertEqual(settings.appid,"32")
