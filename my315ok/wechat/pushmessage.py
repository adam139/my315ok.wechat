# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from cStringIO import StringIO
from PIL import Image
import os
import re
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from my315ok.wechat.interfaces import IwechatSettings
from my315ok.wechat.localapi import check_error
# from my315ok.wechat.tests.test_api import getFile
from bs4 import BeautifulSoup

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__) + "/tests", filename)
    return open(filename, 'r')

def putFile(filename):
    """ using ram disk cache temp file """
    import os
#    COMPILE_MO_FILES = os.environ.get('ramcache', '')
    filename = os.path.join('/ramdisk/', filename)
    return filename


# 适应于 plone ATContenttype content object,using zcml configure multi-adapters
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
#         update_mid = False
        try:
            imgobj = self.image_data(obj)
            imgobj = Image.open(imgobj)
            suffix = (imgobj.format).lower()
            filename = "news.%s" % suffix
            imgfile = putFile(filename)
            imgobj.save(imgfile)
            del imgobj
            filename = open(imgfile,'r')    
        except:  # if can't get obj's image data,then use a  default image
            registry = getUtility(IRegistry)
            settings = registry.forInterface(IwechatSettings)
            import urllib2
            if settings.preview == None:
                filename = getFile("avatar_default.jpg")
            else:
                url = settings.preview
                imgstr = urllib2.urlopen(url).read()
                imgobj = Image.open(StringIO(imgstr))
                suffix = (imgobj.format).lower()
                filename = "news.%s" % suffix
                imgfile = putFile(filename)
                imgobj.save(imgfile)
                del imgobj
                filename = open(imgfile,'r')               
        try:

            rt = api.upload_media('image',filename)                
            rt = check_error(rt)
            filename.close()
            return rt["media_id"]
        except:
            raise Exception("some error:can't upload image")            

    def get_imgobj(self,imgsrc):
        """从 img tag src property构造imgobj        
        parameters: 
            imgsrc is the images origin src,            
        return the image obj
        """
#         update_mid = False
        try:
            import urllib2
            imgstr = urllib2.urlopen(imgsrc).read()
            imgobj = Image.open(StringIO(imgstr))
            suffix = (imgobj.format).lower()
            filename = "news.%s" % suffix
            imgfile = putFile(filename)
            imgobj.save(imgfile)
            del imgobj
            filename = open(imgfile,'r')
        except:                                    
            filename = getFile("avatar_default.jpg")
        return filename                          
 
    def relative2absolute(self,old_src):
        "transfer relative url to absolute url."
        obj = self.obj
        from urlparse import urljoin
#         import pdb
#         pdb.set_trace()
        return  urljoin(obj.absolute_url(), old_src)
        
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
            news_parameters["author"] = obj.getOwner().getUserName()
            news_parameters["title"] = obj.title
            news_parameters["content_source_url"] = obj.absolute_url()
            news_parameters["content"] = text
            news_parameters["digest"] = obj.description
            news_parameters["show_cover_pic"] = "1"
            ars = [] # article array, member item is a news item
            ars.append(news_parameters)
            data = {}
            data["articles"] = ars

            # 临时图文素材
            newsid = api.upload_news(data)
            #永久图文素材
#             newsid = api.add_news(ars)
            del ars   #free ram storage            
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

        output = self.transfer_img(text)
        return output
        
    def transfer_img(self,source):
        "transfer all img tags to tenxun image server through upload permanent api "
#         soup = BeautifulSoup(source,"html.parser")        
#         secondp = soup.new_tag("p",style="text-align:center;color:red")
#         secondp.string = u"长按二维码或扫描即可关注"
#         lastp = soup.new_tag("p",style="text-align:center")
#         qrcode = soup.new_tag("img",src="http://mmbiz.qpic.cn/mmbiz_jpg/n13LXaB2n42z6zLibGAWsmh1pbaAt53MWA7qZQoAc1zhlGae8ODHaUHkCJgvBrJcX6fnWoaL4nd4OjjpzQT6J6w/640?wx_fmt=jpeg&amp;amp;wxfrom=5&amp;amp;wx_lazy=1",alt="qrcode") 
#         lastp.append(qrcode)
#         soup.find_all('p')[-1].insert_after(lastp)
#         soup.find_all('p')[-1].insert_after(secondp)
        soup = self.append_qrcode(source)
        # remove all smallest images
        soup = self.remove_duplicate_imgs(soup)
        imgs = soup.find_all(src=re.compile("^(?!.*mmbiz)"))
        output = {'mid':'','html':''}
        j = 0
        for img in imgs:
            j = j + 1            
            old_src = img['src']
            if len(old_src) == 0:continue
            if not old_src.startswith('http'):
                old_src = self.relative2absolute(old_src)            
            try:
                imgobj = self.get_imgobj(old_src)
                rt = self.api.upload_permanent_media("image",imgobj)
                rt = check_error(rt)
                src = rt['url']
                filename = self.get_imgobj(src)
                rt2 = self.api.upload_media('image',filename)
                rt2 = check_error(rt2)
                filename.close()
                img['src'] = src
                if j == 1:output['mid'] = rt2['media_id']
            except:
                continue
        output['html'] = soup.prettify()
        return  output 

    def append_qrcode(self,source):
        "添加qrcode"
        soup = BeautifulSoup(source,"html.parser")        
        secondp = soup.new_tag("p",style="text-align:center;color:red")
        secondp.string = u"长按二维码或扫描即可关注"
        lastp = soup.new_tag("p",style="text-align:center")
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IwechatSettings)
        if settings.qrcode == None:
            imgurl = "http://mmbiz.qpic.cn/mmbiz_jpg/n13LXaB2n42z6zLibGAWsmh1pbaAt53MWA7qZQoAc1zhlGae8ODHaUHkCJgvBrJcX6fnWoaL4nd4OjjpzQT6J6w/640?wx_fmt=jpeg&amp;amp;wxfrom=5&amp;amp;wx_lazy=1"
        else:
            imgurl = settings.qrcode        
        qrcode = soup.new_tag("img",src=imgurl,alt="qrcode") 
        lastp.append(qrcode)
        soup.find_all('p')[-1].insert_after(lastp)
        soup.find_all('p')[-1].insert_after(secondp)
        return soup
    
    def remove_duplicate_imgs(self,soup):
        "remove small duplicate images"
        # remove all smallest images
        allp = soup.find_all("p",class_="visible-xs-block")       
        for i in allp:
            small = i.extract()
        return soup
    
    def upload_news(self):
            """上传图文消息""" 
            obj = self.obj
            api = self.api
            output = self.text(obj)
            text = output['html']
            news_parameters ={}    # declare a news item parameters
            news_parameters["author"] = obj.getOwner().getUserName()
            news_parameters["title"] = obj.title
            news_parameters["content"] = text
            news_parameters["content_source_url"] = obj.absolute_url()            
            news_parameters["digest"] = obj.description
            news_parameters["show_cover_pic"] = "0"
        
            if output['mid'] != '':
                mid = output['mid']                                 
            else:                   
                mid = self.upload_image(api,obj)           
            news_parameters["thumb_media_id"] = mid
            ars = [] # article array, member item is a news item
            ars.append(news_parameters)
            data = {}
            data["articles"] = ars            
            newsid = api.upload_news(data)  
            newsdic = {}
            newsdic["media_id"] = newsid
            return newsdic      
                
    
    def image_data(self,obj):
        imgobj = StringIO(obj.image.data)
        return imgobj

#适应于dexterity container 
class DexterityContainer(DexterityItem):
    """ send productfolder text and image message as wechat article to flowers."""
    
    def upload_news(self):
            """上传图文消息""" 
            obj = self.obj
            api = self.api
            request = getattr(obj, "REQUEST", None)
            #call product folder view
            folderview = getMultiAdapter((obj, request),name=u"contentlisting")
            subitems = folderview(batch=True, b_size=3,sort_on="created",sort_order="reverse")
            ars = [] # article array, member item is a news item 
            k = 0           
            for brain in subitems:
                k = k+1
                # just fetch three items 
                if k > 3:break    # max is 10 newsitems
                mid = self.upload_image(api,brain.getObject())            
                news_parameters ={}    # declare a news item parameters
                news_parameters["thumb_media_id"] = mid
                news_parameters["author"] = brain.Creator()
                news_parameters["title"] = brain.Title()
                news_parameters["content_source_url"] = brain.getURL()
                news_parameters["content"] = self.text(brain.getObject())
                news_parameters["digest"] = brain.Description()
                news_parameters["show_cover_pic"] = "1"
                ars.append(news_parameters)
            data = {}
            data["articles"] = ars
            del ars   #free ram storage          
            newsid = api.upload_news(data)
            newsdic = {}
            newsdic["media_id"] = newsid
            return newsdic
#适应于my315ok.product 的 prdt folder container 
class PrdtFolderContainer(DexterityItem):
    """ send productfolder text and image message as wechat article to flowers."""
    
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
                # just fetch three items 
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
        