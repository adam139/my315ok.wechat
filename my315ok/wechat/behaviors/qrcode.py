# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.supermodel import model
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from my315ok.wechat import MessageFactory as _
class IQrcode(model.Schema):
    
    form.fieldset(
            'Wechat',
            label=_(u'Wechat'),
            fields=('image','image_caption'),
            )    
    image = namedfile.NamedBlobImage(
            title=_(u"qrcode Image"),
            description=u"",
            required=False,
                    )
    image_caption = schema.TextLine(
            title=_(u"wechat qrcode image"),
            description=u"",
            required=False,
                    )
    form.omitted('image','image_caption') 
alsoProvides(IQrcode, IFormFieldProvider)

class Qrcode(object):
    implements(IQrcode)
    adapts(IDexterityContent)
    
    def __init__(self, context):
        self.context = context

#
#class QrcodeAdapter(grok.Adapter, Qrcode):
#    grok.context(IDexterityContent)
#    grok.implements(IQrcode)        