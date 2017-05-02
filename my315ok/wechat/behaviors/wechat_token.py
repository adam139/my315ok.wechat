"""Behaviours to Add appid appsec token fields for member object."""
from rwproperty import getproperty, setproperty
from zope.interface import implements, alsoProvides
from zope.component import adapts
from zope import schema
from five import grok
from plone.directives import form

from dexterity.membrane.content.member import IMember
from Products.CMFCore.interfaces import IDublinCore
from my315ok.wechat import MessageFactory as _

class IWechatApiKey(form.Schema):
    """Add api authenticate fields to content """
    form.fieldset(
            'Wechat',
            label=_(u'Wechat'),
            fields=('appid','appsecret','token'),
            )
    appid = schema.TextLine(
        title=_(u'label_appid', default=u'Appid'),
        required=True
        )
    appsecret = schema.TextLine(
        title=_(u'label_appsecret', default=u'Appsecret'),
        required=True
        )
    token = schema.TextLine(
        title=_(u'label_token', default=u'Token'),
        required=True
        )
    encoding_aes_key = schema.TextLine(
        title=_(u'label_token', default=u'Token'),
        required=True
        )
                
alsoProvides(IWechatApiKey, form.IFormFieldProvider)

class WechatApiKey(object):
    
#    adapts(IMember)

    def __init__(self, context):
        self.context = context
            
    def _get_appid(self):
        return self.context.appid

    def _set_appid(self, value):
        if isinstance(value, str):
            raise ValueError('appid must be unicode.')
        self.context.appid = value
    appid = property(_get_appid, _set_appid)

    def _get_appsecret(self):
        return self.context.appsecret

    def _set_appsecret(self, value):
        if isinstance(value, str):
            raise ValueError('Appsecret must be unicode.')
        self.context.appsecret = value
    appsecret = property(_get_appsecret, _set_appsecret)

    def _get_encoding_aes_key(self):
        return self.context.appsecret

    def _set_encoding_aes_key(self, value):
        if isinstance(value, str):
            raise ValueError('encoding_aes_key must be unicode.')
        self.context.encoding_aes_key = value
    encoding_aes_key = property(_get_encoding_aes_key, _set_encoding_aes_key)

    def _get_token(self):
        return self.context.token

    def _set_token(self, value):
        if isinstance(value, str):
            raise ValueError('token must be unicode.')
        self.context.token = value
    token = property(_get_token, _set_token)        
        
class WechatApiKeyAdapter(grok.Adapter, WechatApiKey):
    grok.context(IMember)
    grok.implements(IWechatApiKey)  
