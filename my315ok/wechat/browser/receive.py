#-*- coding: UTF-8 -*-
from five import grok
import json
from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from zope import event
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.interfaces import IATNewsItem
from my315ok.wechat.interfaces import ISendWechatEvent
from my315ok.wechat.events import SendWechatEvent
from my315ok.wechat.content.menufolder import IMenufolder
from my315ok.wechat.interfaces import Iweixinapi
from my315ok.wechat.weixinapi import check_error

from Products.statusmessages.interfaces import IStatusMessage


import six
import os
import inspect
import hashlib
import logging
from my315ok.wechat.config import Config, ConfigAttribute
from my315ok.wechat.parser import parse_user_msg
from my315ok.wechat.reply import create_reply,ArticlesReply,WeChatReply,Article
from my315ok.wechat.utilities import to_binary, to_text

__all__ = ['BaseRoBot', 'WeRoBot']


_DEFAULT_CONFIG = dict(
    TOKEN="plone2018"
)


class BaseRoBot(object):
    message_types = ['subscribe', 'unsubscribe', 'click',  'view',  # event
                     'text', 'image', 'link', 'location', 'voice']

    token = ConfigAttribute("TOKEN")
    session_storage = ConfigAttribute("SESSION_STORAGE")

    def __init__(self, token=None, logger=None, enable_session=True, session_storage=None):
        self.config = Config(_DEFAULT_CONFIG)
        self._handlers = dict((k, []) for k in self.message_types)
        self._handlers['all'] = []
        if logger is None:
            import my315ok.wechat.logger
            logger = my315ok.wechat.logger.logger
        self.logger = logger

        if enable_session and session_storage is None:
            from my315ok.wechat.session.filestorage import FileStorage
            session_storage = FileStorage(
                filename=os.path.abspath("werobot_session")
            )
        self.config.update(
            TOKEN=token,
            SESSION_STORAGE=session_storage,

        )

    def handler(self, f):
        """
        Decorator to add a handler function for every messages
        """
        self.add_handler(f, type='all')
        return f

    def text(self, f):
        """
        Decorator to add a handler function for ``text`` messages
        """
        self.add_handler(f, type='text')
        return f

    def image(self, f):
        """
        Decorator to add a handler function for ``image`` messages
        """
        self.add_handler(f, type='image')
        return f

    def location(self, f):
        """
        Decorator to add a handler function for ``location`` messages
        """
        self.add_handler(f, type='location')
        return f

    def link(self, f):
        """
        Decorator to add a handler function for ``link`` messages
        """
        self.add_handler(f, type='link')
        return f

    def voice(self, f):
        """
        Decorator to add a handler function for ``voice`` messages
        """
        self.add_handler(f, type='voice')
        return f

    def subscribe(self, f):
        """
        Decorator to add a handler function for ``subscribe event`` messages
        """
        self.add_handler(f, type='subscribe')
        return f

    def unsubscribe(self, f):
        """
        Decorator to add a handler function for ``unsubscribe event`` messages
        """
        self.add_handler(f, type='unsubscribe')
        return f

    def click(self, f):
        """
        Decorator to add a handler function for ``click`` messages
        """
        self.add_handler(f, type='click')
        return f

    def key_click(self, key):
        """
        Shortcut for ``click`` messages
        @self.key_click('KEYNAME') for special key on click event
        """
        def wraps(f):
            argc = len(inspect.getargspec(f).args)

            @self.click
            def onclick(message, session=None):
                if message.key == key:
                    return f(*[message, session][:argc])
            return f

        return wraps

    def filter(self, *args):
        """
        Shortcut for ``text`` messages
        ``@self.filter("xxx")``, ``@self.filter(re.compile("xxx"))``
        or ``@self.filter("xxx", "xxx2")`` to handle message with special content
        """

        content_is_list = False

        if len(args) > 1:
            content_is_list = True
        else:
            target_content = args[0]
            if isinstance(target_content, six.string_types):
                target_content = to_text(target_content)

                def _check_content(message):
                    return message.content == target_content
            elif hasattr(target_content, "match") and callable(target_content.match):
                # 正则表达式什么的

                def _check_content(message):
                    return target_content.match(message.content)
            else:
                raise TypeError("%s is not a valid target_content" % target_content)

        def wraps(f):
            if content_is_list:
                for x in args:
                    self.filter(x)(f)
                return f
            argc = len(inspect.getargspec(f).args)

            @self.text
            def _f(message, session=None):
                if _check_content(message):
                    return f(*[message, session][:argc])

            return f

        return wraps

    def view(self, f):
        """
        Decorator to add a handler function for ``view event`` messages
        """
        self.add_handler(f, type='view')
        return f

    def add_handler(self, func, type='all'):
        """
        Add a handler function for messages of given type.
        """
        if not callable(func):
            raise ValueError("{} is not callable".format(func))

        self._handlers[type].append((func, len(inspect.getargspec(func).args)))

    def get_handlers(self, type):
        return self._handlers[type] + self._handlers['all']

    def get_reply(self, message):
        """
        Return the raw xml reply for the given message.
        """
        session_storage = self.config["SESSION_STORAGE"]

        id = None
        session = None
        if session_storage and hasattr(message, "source"):
            id = to_binary(message.source)
            session = session_storage[id]

        handlers = self.get_handlers(message.type)

        try:
            for handler, args_count in handlers:
                args = [message, session][:args_count]
                reply = handler(*args)
                if session_storage and id:
                    session_storage[id] = session
                if reply:
                    return reply
        except:
            self.logger.warning("Catch an exception", exc_info=True)

    def check_signature(self, timestamp, nonce, signature):
        sign = [self.config["TOKEN"], timestamp, nonce]

        sign.sort()
        sign = to_binary(''.join(sign))
        sign = hashlib.sha1(sign).hexdigest()
        return sign == signature
    
    
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Robot(BrowserView):
  
    
    def error(self):
        return "errror 403"
    
    def echo(self):
        data = self.request.form
        return data["echostr"]
        
        
    def outxml(self):
#        data = self.request.form

        robot = BaseRoBot(token="plone2018")  
        
        @robot.text
        def echo(message):
#            return "haha"
            a1 = ArticlesReply(message=message,star=True,MsgType="news",ArticleCount=1)
            item = Article(title=u"Plone技术论坛",img="",description="最大的中文Plone技术社区",url="http://plone.315ok.org/")
            a1.add_article(item)
            return a1         


        body =  self.request.keys()[0]

# 分析原始xml，返回名类型message实例            
        message = parse_user_msg(body)
        logging.info("Receive message %s" % message)
#根据信息类型查询已注册的handler,返回被handler装饰的函数，参数为对应类型message实例            
        reply = robot.get_reply(message)
        if not reply:
            robot.logger.warning("No handler responded message %s"
                                    % message)
            return ''
#设置返回文档头            
#            self.request.response.content_type = 'application/xml'
#            self.request.response.content_type = 'text/xml'            
#创建回复消息             
            
        s2 = create_reply(reply, message=message)
#            return self.response2wechat(s2)
        return s2
    
    
    def __call__(self):
        ev = self.request.environ
        data = self.request.form                 
        robot = BaseRoBot(token="plone2018") 
#        import pdb 
#        pdb.set_trace()
        try:
            rn = robot.check_signature(
            data["timestamp"],
            data["nonce"],
            data["signature"]
            )
        except:
            self.index = ViewPageTemplateFile("templates/error.pt")
            return self.index(self) 
            
        if ev['REQUEST_METHOD'] =="GET":
            # valid request from weixin
            if rn:
                self.index = ViewPageTemplateFile("templates/echo.pt")
#                self.request.RESPONSE.setHeader("Content-type", "text/plain")
                     
#                return data["echostr"]
                return self.index(self)
            else:
                self.index = ViewPageTemplateFile("templates/error.pt")

                return self.index(self)           
            
        else:
            # normal request form weixin
            if not rn:
                self.index = ViewPageTemplateFile("templates/error.pt")
#                self.request.RESPONSE.setHeader("Content-type", "text/plain")
                return self.index(self)       # Set header
#        robot = BaseRoBot(token="plone2018")
        self.request.RESPONSE.setHeader("Content-type", "text/xml")
        self.index = ViewPageTemplateFile("templates/outxml.pt")
        return self.index(self)    


class Recieve(grok.View):
    """receive weixin.
    """
    
    grok.context(INavigationRoot)
    grok.name('receive_weixin')
    grok.require('zope2.View')

        
    def abort(self,status):
        template ="""            
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf8" />
            <title>Error: %s</title>
            <style type="text/css">
              html {background-color: #eee; font-family: sans;}
              body {background-color: #fff; border: 1px solid #ddd;
                    padding: 15px; margin: 15px;}
              pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
            </style>
        </head>
        <body>
            <h1>Error: %s</h1>
            <p>微信机器人不可以通过 GET 方式直接进行访问。</p>
        </body>
    </html>
    """ % (status,status) 
        return template   
  
    
    def render(self):
        data = self.request.form
        ev = self.request.environ
        robot = BaseRoBot(token="plone2018")
        
         
        try:
            rn = robot.check_signature(
            data["timestamp"],
            data["nonce"],
            data["signature"]
            )
        except:
            return self.abort(403)
            
        if ev['REQUEST_METHOD'] =="GET":
            # valid request from weixin
            if rn:
                return data["echostr"]
            else:
                return self.abort(403)           
            
        else:
            # normal request form weixin
            if not rn:
                return self.abort(403)
#            import pdb
#            pdb.set_trace()
            body =  self.request.keys()[0]
# 分析原始xml，返回名类型message实例            
            message = parse_user_msg(body)
            logging.info("Receive message %s" % message)
#根据信息类型查询已注册的handler,返回被handler装饰的函数，参数为对应类型message实例            
            reply = robot.get_reply(message)
            if not reply:
                robot.logger.warning("No handler responded message %s"
                                    % message)
                return ''
#设置返回文档头            
#            self.request.response.content_type = 'application/xml'
            self.request.response.content_type = 'text/xml'            
#创建回复消息             
            
            s2 = create_reply(reply, message=message)
#            return self.response2wechat(s2)
            return s2

         
            

