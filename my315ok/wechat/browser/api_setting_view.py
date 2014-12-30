from five import grok
from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.member import IMember
from zope.interface import Interface
#from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity

grok.templatedir('templates')
      
class MembraneMemberView(grok.View):
    grok.context(IMember)     
    grok.template('member_wechat_setting')
    grok.name('wechat_setting')
    grok.require('zope2.View')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
    def available(self):
        available = True if self.context.image else False
        return available
    

from my315ok.wechat.behaviors.wechat_token import IWechatApiKey    
class EditSettings(dexterity.EditForm):
    grok.name('settingsajaxedit')
    grok.context(IMember)
        
    label = _(u'Edit wechat public account settings')            
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IWechatApiKey).select('appid','appsecret','token')       
    
