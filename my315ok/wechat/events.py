#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent

from my315ok.wechat.interfaces import ISendWechatEvent
    
class SendWechatEvent(ObjectEvent):
    interface.implements(ISendWechatEvent)




