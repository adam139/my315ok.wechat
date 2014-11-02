#-*- coding: UTF-8 -*-
from five import grok
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent

from Products.ATContentTypes.interfaces import IATNewsItem
from my315ok.wechat.interfaces import Iweixinapi
from my315ok.wechat.events import ISendWechatEvent
from my315ok.wechat.weixinapi import check_error
from my315ok.wechat.tests.test_api import putFile

from cStringIO import StringIO
from PIL import Image
        
@grok.subscribe(IATNewsItem, ISendWechatEvent)
def sendnews(obj, event):
        """send the news as message of the Wechat"""
        api = Iweixinapi(obj)
    # create articles data
        text = obj.getText()
        import pdb
        pdb.set_trace()
        imgobj = StringIO(obj.getImage().data)

        imgobj = Image.open(imgobj)
        filename = "news.%s" % (imgobj.format).lower()
        imgfile = putFile(filename)
        imgobj.save(imgfile)
#        imgobj = getFile('image.jpg')
        filename = open(imgfile,'r')
        rt = api.upload_media('image',filename)
        del imgobj
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

        
           
        