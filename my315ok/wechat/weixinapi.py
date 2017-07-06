# -*- coding: utf-8 -*-
from five import grok
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope.component import getUtility
import time
import requests
from requests.compat import json as _json
from my315ok.wechat.utilities import to_text
from plone.registry.interfaces import IRegistry
from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat.interfaces import ISendCapable
from my315ok.wechat.interfaces import ISendAllCapable
from my315ok.wechat.interfaces import Iweixinapi
from my315ok.wechat.interfaces import IweixinapiMember
from my315ok.wechat.interfaces import IMemberWeiXinApi

from dexterity.membrane.content.member import IMember
try:
    from werobot.client import Client
except:
    from my315ok.wechat.localapi import Client 

from werobot.robot import _DEFAULT_CONFIG
from werobot.config import Config, ConfigAttribute

 
class BaseApi(Client):
    """参数appid,appsecret通过控制面板配置参数传入，或者用默认值
    """
    implements(Iweixinapi)
    adapts(ISendAllCapable)
        
    def __init__(self,context):
        self.cotext = context
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        self.config = Config(_DEFAULT_CONFIG)
        token = settings.token
        if not bool(token):token = "plone2018"
        app_id = settings.appid
        if not bool(app_id):app_id = "wx08178af75244cb5d" 
        app_secret = settings.appsecret
        if not bool(app_secret):app_secret = "502408a50b79bfafa5f354d99d204dc7"
        encoding_aes_key = settings.encoding_aes_key
        self.config.update(
                TOKEN=token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
                ENCODING_AES_KEY=encoding_aes_key
            ) 
        self._token = None
        self.token_expires_at = None
        

class WeiXinApi(Client):
    """参数appid,appsecret通过member object 传入
    """
    implements(IweixinapiMember)
    adapts(ISendAllCapable,IMember)
        
    def __init__(self,context,member):
        self.cotext = context
        self.member = member
        self.config = Config(_DEFAULT_CONFIG)
        token = member.token
        app_id = member.appid
        app_secret = member.appsecret
        encoding_aes_key = member.encoding_aes_key
        self.config.update(
                TOKEN=token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
                ENCODING_AES_KEY=encoding_aes_key
            ) 
        self._token = None
        self.token_expires_at = None        
                   
class MemberWeiXinApi(Client):
    """参数appid,appsecret通过member object传入
    """
    implements(IMemberWeiXinApi)
    adapts(IMember)
        
    def __init__(self,context):
        self.cotext = context
        self.config = Config(_DEFAULT_CONFIG)
        token = context.token
        app_id = context.appid
        app_secret = context.appsecret
        encoding_aes_key = context.encoding_aes_key
        self.config.update(
                TOKEN=token,
                APP_ID=app_id,
                APP_SECRET=app_secret,
                ENCODING_AES_KEY=encoding_aes_key
            ) 
        self._token = None
        self.token_expires_at = None             
            
