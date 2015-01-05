# -*- coding: utf-8 -*-
"""Behaviours to Add processor appsec logtext fields for member object."""
from rwproperty import getproperty, setproperty
from zope.interface import implements, alsoProvides
from zope.component import adapts
from zope import schema
from five import grok
from plone.directives import form

from dexterity.membrane.content.member import IMember
from Products.CMFCore.interfaces import IDublinCore
from my315ok.wechat import MessageFactory as _

class IWechatLog(form.Schema):
    """Add api authenticate fields to content """
    form.fieldset(
            'Wechat',
            label=_(u'Wechat'),
            fields=('processor','created','logtext'),
            )
    processor = schema.TextLine(
        title=_(u'processor', default=u'processor'),
        required=True
        )
    created = schema.TextLine(
        title=_(u'created time', default=u'created time'),
        required=True
        )
    logtext = schema.TextLine(
        title=_(u'log text', default=u'log text'),
        required=True
        )        
alsoProvides(IWechatLog, form.IFormFieldProvider)

class WechatLog(object):
    
#    adapts(IMember)

    def __init__(self, context):
        self.context = context
            
    def _get_processor(self):
        return self.context.processor

    def _set_processor(self, value):
        if isinstance(value, str):
            raise ValueError('processor must be unicode.')
        self.context.processor = value
    processor = property(_get_processor, _set_processor)

    def _get_created(self):
        return self.context.created

    def _set_created(self, value):
        if isinstance(value, str):
            raise ValueError('Appsecret must be unicode.')
        self.context.created = value
    created = property(_get_created, _set_created)

    def _get_logtext(self):
        return self.context.logtext

    def _set_logtext(self, value):
        if isinstance(value, str):
            raise ValueError('logtext must be unicode.')
        self.context.logtext = value
    logtext = property(_get_logtext, _set_logtext)        
        

