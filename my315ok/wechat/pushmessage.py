# -*- coding: utf-8 -*-
#from zope.component import getMultiAdapter
from cStringIO import StringIO
from PIL import Image

from my315ok.wechat.weixinapi import check_error
from my315ok.wechat.tests.test_api import putFile,getFile
# 适应于 plone news item content object
class Content(object):
    def __init__(self, api,obj):
        self.api = api
        self.obj = obj
        
    def image_data(self,obj):
        imgobj = StringIO(obj.getImage().data)
        return imgobj
        
    def upload_image(self,api,obj):
        """上载内容obj的图像字段到微信server，返回mediaid
        upload current object's image field to wechat server as image media,
        parameters: 
            context is current object that contained a images field,
            api is weixin api,
        return mediaid
        """

        try:
            imgobj = self.image_data(obj)
            imgobj = Image.open(imgobj)
            suffix = (imgobj.format).lower()
            filename = "news.%s" % suffix
            imgfile = putFile(filename)
            imgobj.save(imgfile)
            del imgobj
            filename = open(imgfile,'r')
    
        except:  # if can't get image data,then use a  default image
            filename = getFile("avatar_default.jpg")

        try:
            rt = api.upload_media('image',filename)
            filename.close()
            rt = check_error(rt)
            mid = rt["media_id"]
            return mid
        except:
            raise Exception("some error:can't upload image")            
        
    def text(self,obj):
        text = obj.getText()
        return text
        
    def upload_news(self):
            """上传图文消息""" 
            obj = self.obj
            api = self.api
            text = self.text(obj)

            mid = self.upload_image(api,obj)            
            news_parameters ={}    # declare a news item parameters
            news_parameters["thumb_media_id"] = mid
            news_parameters["author"] = "admin"
            news_parameters["title"] = obj.title
            news_parameters["content_source_url"] = obj.absolute_url()
            news_parameters["content"] = text
            news_parameters["digest"] = obj.description
            news_parameters["show_cover_pic"] = "1"
            ars = [] # article array, member item is a news item
            ars.append(news_parameters)
            data = {}
            data["articles"] = ars
            del ars   #free ram storage   
        
            newsid = api.upload_news(data)
            newsdic = {}
            newsdic["media_id"] = newsid
            return newsdic 

#适应于dexterity item 
class DexterityItem(Content):
    
    def text(self,obj): #may be richtext field
        try:
            text = obj.text.output
        except:
            text = obj.text
        return text
        
    def image_data(self,obj):
        imgobj = StringIO(obj.image.data)
        return imgobj


#适应于dexterity container 
class DexterityContainer(DexterityItem):
    
    def upload_news(self):
            """上传图文消息""" 
            obj = self.obj
            api = self.api
            request = getattr(obj, "REQUEST", None)
            #call product folder view
            folderview = getMultiAdapter((obj, request),name=u"view")
            subitems = folderview.prdt_images()
            ars = [] # article array, member item is a news item 
            k = 0           
            for brain in subitems:
                k = k+1
                if k > 3:break    # max is 10 newsitems

                mid = self.upload_image(api,brain.getObject())            
                news_parameters ={}    # declare a news item parameters
                news_parameters["thumb_media_id"] = mid
                news_parameters["author"] = "admin"
                news_parameters["title"] = brain.Title
                news_parameters["content_source_url"] = brain.getPath()
                news_parameters["content"] = brain.text
                news_parameters["digest"] = brain.Description
                news_parameters["show_cover_pic"] = "1"
                ars.append(news_parameters)
            data = {}
            data["articles"] = ars
            del ars   #free ram storage   
        
            newsid = api.upload_news(data)
            newsdic = {}
            newsdic["media_id"] = newsid
            return newsdic                
        