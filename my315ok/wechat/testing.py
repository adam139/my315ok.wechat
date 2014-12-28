from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class SitePolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import my315ok.products
        xmlconfig.file('configure.zcml', my315ok.products, context=configurationContext)
        import dexterity.membrane
        xmlconfig.file('configure.zcml', dexterity.membrane, context=configurationContext)                
        import my315ok.wechat
        xmlconfig.file('configure.zcml', my315ok.wechat, context=configurationContext)
        
        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'Products.PythonField')
        z2.installProduct(app, 'Products.TALESField')
        z2.installProduct(app, 'Products.TemplateFields')
        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'Products.membrane')        
    
    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.PloneFormGen')
        z2.uninstallProduct(app, 'Products.TemplateFields')
        z2.uninstallProduct(app, 'Products.TALESField')
        z2.uninstallProduct(app, 'Products.PythonField')
        z2.uninstallProduct(app, 'Products.membrane')        
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'my315ok.products:default')        
        applyProfile(portal, 'my315ok.wechat:default')
        applyProfile(portal, 'dexterity.membrane:default')        

FIXTURE = SitePolicy()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="Site:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name="Site:Functional")

from .parser import parse_user_msg

__all__ = ['WeTest']


class WeTest(object):
    def __init__(self, app):
        self._app = app

    def send_xml(self, xml):
        message = parse_user_msg(xml)
        return self._app.get_reply(message)