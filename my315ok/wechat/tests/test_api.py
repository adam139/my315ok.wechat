# -*- coding: utf-8 -*-
import unittest2 as unittest
#from eisoo.mpsource.interfaces import IUserLocator
from my315ok.wechat.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles

from my315ok.wechat.interfaces import Iweixinapi
from my315ok.wechat.weixinapi import check_error
from my315ok.wechat.events import SendWechatEvent
from Products.ATContentTypes.interfaces import IATNewsItem
from Products.ATContentTypes.content.newsitem import ATNewsItem
from plone.namedfile.file import NamedImage
from zope import event
import os
import json
from cStringIO import StringIO
from PIL import Image


def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

def putFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return filename
#    return open(filename, 'r+')
class setupbase(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1',
                             PerPagePrdtNum=2,title="productfolder1",description="demo productfolder")     
     
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="Gif image",description="a gif image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2',title="Jpeg image",description="a jpeg image")
#        portal['productfolder1'].invokeFactory('my315ok.products.product','product3',title="Png image",description="a png image")        

        data = getFile('image.gif').read()
        item = portal['productfolder1']['product1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        item.text = "<p>test send dexterity object</p>"        
        data2 = getFile('image.jpg').read()        
        item2 = portal['productfolder1']['product2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')
        item2.text = "<p>test send dexterity object</p>"  

        portal.invokeFactory('News Item','news1',
                                         title=u"news1",
                                         description=u"a news",
                                         text='news',

                                         )
        portal.invokeFactory('Document','page1',
                                         title=u"page1",
                                         description=u"a document",
                                         text='<p>document</p>',

                                         )        
        data = getFile('image.jpg').read()
        item = portal['news1']
        item.setImage(data, content_type="image/jpg")

        self.portal = portal

        from my315ok.wechat.interfaces import ISendCapable
        obj = portal['news1']
        if not(ISendCapable.providedBy(obj)):
            from zope.interface import alsoProvides
            alsoProvides(obj,ISendCapable)
        self.api = Iweixinapi(obj)        
#        self.api = Iweixinapi(portal['news1'])    

class Allcontents(setupbase):
    layer = INTEGRATION_TESTING   

    
    def test_config(self):
        item = self.portal['news1']
        appid = "appid"
        self.assertEqual(Iweixinapi(item).appid,appid)
        
    def test_token(self):
        item = self.portal['news1']
        json = Iweixinapi(item).grant_token()

        expires = json["expires_in"]
        self.assertEqual(expires,7200)
        
    def test_createmenu(self):
        #create a menu

        rjson = self.api.create_menu(menu_data)
        code = rjson['errcode']
        self.assertEqual(code,0)
        
        
    def test_getmenu(self):
        getjson = self.api.get_menu()
        menu_data = {
                "button":[
                    {
                        "type":"click",
                        "name":"今日歌曲",
                        "key":"V1001_TODAY_MUSIC"
                    },
                    {
                        "type":"click",
                        "name":"歌手简介",
                        "key":"V1001_TODAY_SINGER"
                    },
                    {
                        "name":"菜单",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"搜索",
                                "url":"http://www.soso.com/"
                            },
                            {
                                "type":"view",
                                "name":"视频",
                                "url":"http://v.qq.com/"
                            },
                            {
                                "type":"click",
                                "name":"赞一下我们",
                                "key":"V1001_GOOD"
                            }
                        ]
                    }
                ]}

        fst = getjson['menu']['button'][1]['name']
        orig = menu_data['button'][1]['name'].decode()        
#        djson = json.dumps(menu_data).decode("utf-8")
        self.assertEqual(fst,orig)
        
    def test_uploadmedia(self):
        imgobj = getFile('image.jpg')
        
#        imgobj =  StringIO(imgobj.read())
        upreturn = self.api.upload_media('image',imgobj)
        imgobj.close()
#        import pdb
#        pdb.set_trace()
        self.assertEqual('image',upreturn['type'])
        
        
    def test_sendtext(self):
        "send text message" 
        item = self.portal['news1']
        text = item.getText()
        try:
            followers = self.api.get_followers()['data']['openid']
        except:
            raise ("some error")

        for toid in followers:
            self.api.send_text_message(toid,text)
        
#测试按openid群发图dexterity content object: product   
    def test_sendnews_article(self):
        item = self.portal['productfolder1']
        event.notify(SendWechatEvent(item))

#测试按openid群发图dexterity content object: product   
    def test_sendnews_prod(self):
        item = self.portal['productfolder1']['product2']
        event.notify(SendWechatEvent(item))

#测试按openid群发图dexterity content object: product   
    def test_sendnews_page(self):
        item = self.portal['page1']
        event.notify(SendWechatEvent(item))

#测试按openid群发图文消息    
    def test_sendnews(self):
        item = self.portal['news1']
        event.notify(SendWechatEvent(item))
#        text = item.getText()
#        import pdb
#        pdb.set_trace()
#        imgobj = StringIO(item.getImage().data)
#
#        imgobj = Image.open(imgobj)
#        filename = "news.%s" % (imgobj.format).lower()
#        imgfile = putFile(filename)
#        imgobj.save(imgfile)
##        imgobj = getFile('image.jpg')
#        filename = open(imgfile,'r')
#        rt = self.api.upload_media('image',filename)
#        del imgobj
#        filename.close()
#        rt = check_error(rt)
#        mid = rt["media_id"]
#        news_parameters ={}
#        news_parameters["thumb_media_id"] = mid
#        news_parameters["author"] = "admin"
#        news_parameters["title"] = item.title
#        news_parameters["content_source_url"] = item.absolute_url()
#        news_parameters["content"] = text
#        news_parameters["digest"] = item.description
#        news_parameters["show_cover_pic"] = "1"
#        ars = []
#        ars.append(news_parameters)
#        data = {}
#        data["articles"] = ars
#        del ars      
#        
#        newsid = self.api.upload_news(data)
#        newsdic = {}
#        newsdic["media_id"] = newsid
#        data = {}
#        try:
#            followers = self.api.get_followers()['data']['openid']
#        except:
#            raise ("some error")        
#        data["touser"] = followers
#        data["mpnews"] = newsdic
#        data["msgtype"] = "mpnews"
#        
#        self.api.send_by_openid(data)
#        self.assertEqual(imgobj,getFile('image.jpg').read())
       # 二维码测试
    def test_qrcode(self):
        """first create forever qrcode,second generate a qrcode image.
        data:{"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": 123}}}
        """

        data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": 123}}}
        qr = self.api.create_qrcode(data)
        try:
            ticket=check_error(qr)['ticket']
            import pdb
            pdb.set_trace()
            rt = self.api.show_qrcode(ticket)
            # image data
            virf = StringIO(rt.content)
            imgobj = Image.open(virf)
            filename = "qrcode.jpg" 
            imgfile = putFile(filename)
            imgobj.save(imgfile)

        except:
            raise Exception("show qrcode error")
        
        
                
      
    
        