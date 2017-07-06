# -*- coding: utf-8 -*-
import unittest
#from eisoo.mpsource.interfaces import IUserLocator
from my315ok.wechat.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles

from my315ok.wechat.interfaces import Iweixinapi,IweixinapiMember
from my315ok.wechat.localapi import check_error
from my315ok.wechat.events import SendWechatEvent,SendAllWechatEvent,SendSelfWechatEvent

from plone.namedfile.file import NamedImage
# from plone.namedfile import field as namedfile
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
def dummy_image():
    from plone.namedfile.file import NamedBlobImage
    filename = os.path.join(os.path.dirname(__file__), u'image.jpg')
    return NamedBlobImage(
        data=open(filename, 'r').read(),
        filename=filename
    )
    
class setupbase(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('Folder', 'container1',
                             title="container1",description="container1")
        portal.invokeFactory('Folder', 'container2',
                             title="container2",description="container2")             
        
        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1',
                             PerPagePrdtNum=2,title="productfolder1",description="demo productfolder")     
     
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="Gif image",description="a gif image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2',title="Jpeg image",description="a jpeg image")
#        portal['productfolder1'].invokeFactory('my315ok.products.product','product3',title="Png image",description="a png image")        

        data = getFile('image.png').read()
        item = portal['productfolder1']['product1']
        item.image = NamedImage(data, 'image/png', u'image.png')
        item.text = "<p>test send dexterity object</p>"
        item.reindexObject(idxs=["text"])        
        data2 = getFile('image.jpg').read()        
        item2 = portal['productfolder1']['product2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')
        item2.text = "<p>test send dexterity object</p>"
        item2.reindexObject(idxs=["text"])            

        portal['container1'].invokeFactory('News Item','news1',
                                         title=u"news1",
                                         description=u"a news",
                                         text='<strong>news1</strong><span style="color:red">this is test</span>',
                                         )
        portal['container1'].invokeFactory('News Item','news2',
                                         title=u"news2",
                                         description=u"a news 2",
                                         text='news2',
                                         )        
        portal['container1'].invokeFactory('Document','page1',
                                         title=u"page1",
                                         description=u"a document",
                                         text='<p>document</p>',

                                         )        
        data = getFile('image.jpg').read()
        item = portal['container1']['news1']
        item.image = dummy_image() 
        item.image_caption = "news image"
#         item.setImage(data, content_type="image/jpg")
# create member object        
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder')
        
        portal['memberfolder'].invokeFactory('dexterity.membrane.member', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1",
                             appid="wx77d2f3625808f911",
                             appsecret="b66e860a24452f782dc40d3daab6a79a",
                             encoding_aes_key = "",
                             token="plone2018")     
     
          
 
        data = getFile('image.jpg').read()
        item = portal['memberfolder']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')        

        self.portal = portal
        from my315ok.wechat.interfaces import ISendCapable
        obj = portal['container1']['news1']
#        import pdb
#        pdb.set_trace()
        if not(ISendCapable.providedBy(obj)):
            from zope.interface import alsoProvides
            alsoProvides(obj,ISendCapable)
        self.api = Iweixinapi(obj)        
#        self.api = Iweixinapi(portal['news1'])    

class Allcontents(setupbase):
    layer = INTEGRATION_TESTING   

    
    def test_config(self):
        item = self.portal['container1']['news1']
        appid = "wx77d2f3625808f911"
        self.assertEqual(Iweixinapi(item).appid,appid)
        
    def test_token(self):
        item = self.portal['container1']['news1']
        json = Iweixinapi(item).grant_token()

        expires = json["expires_in"]
        self.assertEqual(expires,7200)
        
    def test_createmenu(self):
        #create a menu
        menu_data = {
                "button":[
                    {
                        "type":"click",
                        "name":"信息公开",
                        "key":"xinxigongkai",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"通知公告",
                                "url":"http://www.xtshzz.org/xinxigongkai/tongzhigonggao"
                            },
                            {
                                "type":"view",
                                "name":"政策法规",
                                "url":"http://www.xtshzz.org/xinxigongkai/zhengcefagui"
                            }
                        ]
                    },
                    {
                        "type":"click",
                        "name":"新闻中心",
                        "key":"xinwenzhongxin",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"工作动态",
                                "url":"http://www.xtshzz.org/xinwenzhongxin/guanligongzuodongtai"
                            },
                            {
                                "type":"view",
                                "name":"组织风采",
                                "url":"http://www.xtshzz.org/xinwenzhongxin/shehuizuzhifengcai"
                            }
                        ]
                    },
                    {
                        "name":"指尖支部",
                        "type":"click",
                        "key":"zhijianzhibu",
                        "sub_button":[
                            {
                                "type":"view",
                                "name":"党建信息",
                                "url":"http://www.xtshzz.org/zhijianzhibu/dangjianxinxi"
                            },
                            {
                                "type":"view",
                                "name":"党务管理",
                                "url":"http://www.xtshzz.org/zhijianzhibu/dangwuguanli"
                            },
                            {
                                "type":"view",
                                "name":"在线培训",
                                "url":"http://www.xtshzz.org/zhijianzhibu/zaixianpeixun"
                            }
                        ]
                    }
                ]}
        
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

        orig = menu_data['button'][1]['name'].decode('utf-8')        
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
        
        
    def test_upload_permanent_media(self):
        imgobj = getFile('image.jpg')
#         data = {}
#         data["type"] = "image"
#         media = {}
#         media["media"] = "@%s" % os.path.join(os.path.dirname(__file__), 'image.jpg')
#         data["media"] = media
        rt = self.api.upload_permanent_media("image",imgobj)
        import pdb
        pdb.set_trace()
        self.assertTrue('' != rt['url'])
        
    def test_sendtext(self):
        "send news text message" 
        item = self.portal['container1']['news1']
        try:
            text = item.text.output
        except:
            text = item.text
        try:
            followers = self.api.get_followers()['data']['openid']

        except:
            raise ("can't get followers.")
            return
        for toid in followers:
            self.api.send_text_message(toid,text)
        
#测试按openid群发图dexterity content object: product   
    def test_selfsendnews_article(self):
        item = self.portal['productfolder1']
        event.notify(SendSelfWechatEvent(item))


#测试按openid群发图dexterity content object: product   
    def test_news_send(self):
        item = self.portal['container1']['news1']
        event.notify(SendWechatEvent(item))
    def test_prod_send(self):
        item = self.portal['productfolder1']['product2']
        import pdb
        pdb.set_trace()
        event.notify(SendWechatEvent(item))    
    def test_articles_send(self):
        item = self.portal['container1']
        event.notify(SendWechatEvent(item))
#测试按openid群发图dexterity content object: product   
    def test_productfolder_send(self):
        item = self.portal['productfolder1']
        event.notify(SendWechatEvent(item))
#测试按openid群发图dexterity content object: product   
    def test_allsendnews_prod(self):
        item = self.portal['productfolder1']['product2']
        event.notify(SendAllWechatEvent(item))        



       # 二维码测试
    def test_qrcode(self):
        """first create forever qrcode,second generate a qrcode image.
        data:{"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": 123}}}
        """

        data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": 123}}}
        qr = self.api.create_qrcode(data)
        try:
            ticket=check_error(qr)['ticket']

            rt = self.api.show_qrcode(ticket)
            # image data
            virf = StringIO(rt.content)
            imgobj = Image.open(virf)
            filename = "qrcode2.jpg" 
            imgfile = putFile(filename)
            imgobj.save(imgfile)
        except:
            raise Exception("show qrcode error")
        
    def test_ajax_download_qrcode(self):
        from zope.component import getUtility
        from plone.keyring.interfaces import IKeyManager
        import json
        import hmac
        from hashlib import sha1 as sha
        from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
        from plone.testing.z2 import Browser                
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'id': 'member1',                                                                       
                        }
# Look up and invoke the view via traversal
        view = self.portal['memberfolder']['member1'].restrictedTraverse('@@ajaxuploadqrcode')
        result = view()
        self.assertEqual(json.loads(result)['info'],1)        
                
      
    
        