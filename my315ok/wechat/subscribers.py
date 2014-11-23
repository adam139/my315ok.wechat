#-*- coding: UTF-8 -*-
from five import grok
from zope import event

from Products.ATContentTypes.interfaces import IATNewsItem
from my315ok.wechat.interfaces import Iweixinapi

from my315ok.wechat.events import ISendWechatEvent,IReceiveWechatEvent
#from Products.ATContentTypes.interfaces import IATNewsItem
from my315ok.wechat.weixinapi import check_error
from my315ok.wechat.tests.test_api import putFile,getFile

from cStringIO import StringIO
from PIL import Image

from plone.dexterity.utils import createContentInContainer          

@grok.subscribe(IReceiveWechatEvent)
def ReceiveWechatEvent(eventobj):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    
    from my315ok.wechat.browser.receive import BaseRoBot,StoreMessage 
    from Products.ATContentTypes.interfaces import IATNewsItem
    from zope.site.hooks import getSite
    from Products.CMFCore.utils import getToolByName
    from my315ok.wechat.events import SendWechatEvent
    site = getSite()
    robot = BaseRoBot(token="plone2018")
    
    @robot.text
    def echo(message):        
        catalog = getToolByName(site,'portal_catalog')
        try:
            newest = catalog.unrestrictedSearchResults({'object_provides': IATNewsItem.__identifier__})
            return newest[0].getObject()
        except:
            return

              
    reply = robot.get_reply(eventobj.message)
    del robot
#    event.notify(SendWechatEvent(reply))
    
    storer = StoreMessage()
    # 文本消息，保存为textmessage对象
    @storer.text
    def create_text_message(message):
        folder = storer.get_folder(site)
        mid = str(message.id)
        contenttype = "my315ok.wechat.content.textmessage" 
        try:
            item =createContentInContainer(folder,contenttype,checkConstraints=False,id=mid)
            item.Content = message.content
            item.FromUserName = message.source
            item.MsgType = "text"
            item.MsgId = mid
            return True            
        except:
            return  False
            

    return storer.store_message(eventobj.message)


@grok.subscribe(IATNewsItem, ISendWechatEvent)
def sendnews(obj, event):
        """send the news as message of the Wechat"""
        api = Iweixinapi(obj)
    # create articles data
        text = obj.getText()
#        import pdb
#        pdb.set_trace()
        try:
            imgobj = StringIO(obj.getImage().data)
            imgobj = Image.open(imgobj)
            suffix = (imgobj.format).lower()
            filename = "news.%s" % suffix
            imgfile = putFile(filename)
            imgobj.save(imgfile)
            del imgobj
#        imgobj = getFile('image.jpg')
            filename = open(imgfile,'r')
        except:
            filename = getFile("avatar_default.jpg")
        rt = api.upload_media('image',filename)

        filename.close()
        rt = check_error(rt)
        mid = rt["media_id"]
        news_parameters ={}
        news_parameters["thumb_media_id"] = mid
        news_parameters["author"] = "admin"
        news_parameters["title"] = obj.title
        news_parameters["content_source_url"] = obj.absolute_url()
        news_parameters["content"] = text
        news_parameters["digest"] = obj.description
        news_parameters["show_cover_pic"] = "1"
        ars = []
        ars.append(news_parameters)
        data = {}
        data["articles"] = ars
        del ars      
        
        newsid = api.upload_news(data)
        newsdic = {}
        newsdic["media_id"] = newsid
        data = {}
        try:
            followers = api.get_followers()['data']['openid']
        except:
            raise ("some error")        
        data["touser"] = followers
        data["mpnews"] = newsdic
        data["msgtype"] = "mpnews"        
        api.send_by_openid(data)

        
           
        