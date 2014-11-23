#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent

from my315ok.wechat.interfaces import ISendWechatEvent
from my315ok.wechat.interfaces import IReceiveWechatEvent
    
class SendWechatEvent(ObjectEvent):
    interface.implements(ISendWechatEvent)


class ReceiveWechatEvent(object):
    interface.implements(IReceiveWechatEvent)

    def __init__(self,message):
        """message objdect """
        self.message = message    

