#-*- coding: UTF-8 -*-
from five import grok
from zope import event
import zope.interface
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
try:
    from plone.app.contenttypes.interfaces import INewsItem    
except:
    from Products.ATContentTypes.interfaces import IATNewsItem as INewsItem
try:
    from plone.app.contenttypes.interfaces import IDocument
except:
    from  Products.ATContentTypes.interfaces import IATDocument as IDocument        

from plone.app.contenttypes.interfaces import IFolder
from plone.dexterity.interfaces import IDexterityContent
from my315ok.wechat.interfaces import Iweixinapi
from my315ok.wechat.interfaces import IweixinapiMember
from my315ok.wechat.events import ISendWechatEvent
from my315ok.wechat.events import ISendAllWechatEvent
from my315ok.wechat.events import ISendSelfWechatEvent
from my315ok.wechat.events import IReceiveWechatEvent
from my315ok.products.product import Iproduct
from my315ok.products.productfolder import Iproductfolder
from plone.dexterity.utils import createContentInContainer          
from my315ok.wechat.pushmessage import Content
from my315ok.wechat.pushmessage import DexterityItem
from my315ok.wechat.pushmessage import DexterityContainer
from dexterity.membrane.content.member import IMember

@grok.subscribe(IReceiveWechatEvent)
def ReceiveWechatEvent(eventobj):
    """this event be fired when a message arrived wechat platform"""    
    from my315ok.wechat.browser.receive import BaseRoBot,StoreMessage 
    from Products.ATContentTypes.interfaces import IATNewsItem
    from zope.site.hooks import getSite
    from Products.CMFCore.utils import getToolByName
    from my315ok.wechat.events import SendWechatEvent
    site = getSite()
    # 答复消息
    robot = BaseRoBot(token="plone2018")   
    
    #we directly answer a news item to client when we receive a text type message.
    @robot.text
    def echo(message):        
        catalog = getToolByName(site,'portal_catalog')
        try:
            newest = catalog.unrestrictedSearchResults({'object_provides': INewsItem.__identifier__})
            return newest[0].getObject()
        except:
            return              
    reply = robot.get_reply(eventobj.message)
    del robot

  # 保存消息    
    storer = StoreMessage()
    # 文本消息handler，保存为textmessage对象
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


@grok.subscribe(zope.interface.Interface, ISendWechatEvent)
def sendnews(obj, event):
        """send obj's content as message of the Wechat through system wechat account"""
        from my315ok.wechat.interfaces import ISendCapable
        if not(ISendCapable.providedBy(obj)):
            from zope.interface import alsoProvides
            alsoProvides(obj,ISendCapable)
        api = Iweixinapi(obj)
    # if news item create articles data (INewsItem)
        if INewsItem.providedBy(obj) or Iproduct.providedBy(obj):
            # get context's adapter object
            at = DexterityItem(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("can't get flowers")        
            data["touser"] = followers
#            data["mpnews"] = newsdic
            data["mpnews"] = at.upload_news()           
            data["msgtype"] = "mpnews"        
            api.mass_send(data)            
        elif  IDocument.providedBy(obj):
            text = at.text(obj)
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")
            data["touser"] = followers
            data["msgtype"] = "text"
            data["text"] = {"content":text}
            api.mass_send(data)                              
    # if is dexterity content object
        elif IFolder.providedBy(obj):
            at = DexterityContainer(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            
            data["touser"] = followers
            data["mpnews"] = at.upload_news()           
            data["msgtype"] = "mpnews"        
            api.mass_send(data)
                        
        elif  Iproductfolder.providedBy(obj):
            atnews = DexterityContainer(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.mass_send(data)
        else:
            pass                              
                          
def getAllMember(obj):
    """call member_folderview for get all dexterity member brains"""
    from Products.CMFCore.utils import getToolByName
    from dexterity.membrane.content.memberfolder import IMemberfolder 
    from dexterity.membrane.content.member import IMember   
    request = getattr(obj, "REQUEST", None)
    # fetch member folder object
    catalog = getToolByName(obj, "portal_catalog")
    brains = catalog(object_provides=IMemberfolder.__identifier__)
    folder = brains[0].getObject()    
    folderview = queryMultiAdapter((folder, request),name=u"admin_view")
    subitems = folderview.getMemberBrains()   
    return subitems

@grok.subscribe(zope.interface.Interface, ISendAllWechatEvent)
def pushAllWeixin(obj, event):
    """send obj's content as message of the Wechat"""
    from my315ok.wechat.interfaces import ISendAllCapable
    import time
    if not(ISendAllCapable.providedBy(obj)):
        from zope.interface import alsoProvides
        alsoProvides(obj,ISendAllCapable)        
        
    if INewsItem.providedBy(obj):        
        for member in getAllMember(obj):
#            import pdb
#            pdb.set_trace()
            member = member.getObject()
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: break
            atnews = Content(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
            time.sleep(5)            
    elif IDocument.providedBy(obj):
        for member in getAllMember(obj): 
            member = member.getObject()            
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: break
            text = obj.getText()
            try:
                followers = self.api.get_followers()['data']['openid']
            except:
                raise Exception("some error")
            for toid in followers:
                self.api.send_text_message(toid,text)
                # if is dexterity content object
    elif Iproduct.providedBy(obj):
        for member in getAllMember(obj): 
            member = member.getObject()            
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: break
            atnews = DexterityItem(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
    elif Iproductfolder.providedBy(obj):
        for member in getAllMember(obj): 
            member = member.getObject()
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: break
            atnews = DexterityContainer(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
    else:
        pass                                        
      
@grok.subscribe(zope.interface.Interface, ISendSelfWechatEvent)
def pushSelfWeixin(obj, event):
    """send obj's content as message of the Wechat to myself followers"""
    from my315ok.wechat.interfaces import ISendAllCapable
    import time
    if not(ISendAllCapable.providedBy(obj)):
        from zope.interface import alsoProvides
        alsoProvides(obj,ISendAllCapable)        
    pm = getToolByName(obj, "portal_membership")
    member = pm.getAuthenticatedMember()
    member_id = member.getId()
#    catalog = getToolByName(obj, "portal_catalog")
#    memberbrains = catalog(object_provides=IMember.__identifier__,email=member_id)
    memberbrains = getAllMember(obj)
    if len(memberbrains) ==0:return    
    for bn in memberbrains:
        if bn.email == member_id:break
    member = bn.getObject()         
    if INewsItem.providedBy(obj) or IDocument.providedBy(obj):
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: return
            atnews = Content(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
            time.sleep(5)            
    elif IDocument.providedBy(obj):           
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: return
            text = obj.getText()
            try:
                followers = self.api.get_followers()['data']['openid']
            except:
                raise Exception("some error")
            for toid in followers:
                self.api.send_text_message(toid,text)
                # if is dexterity content object
    elif Iproduct.providedBy(obj):           
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: return
            atnews = DexterityItem(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
    elif Iproductfolder.providedBy(obj):
            api = queryMultiAdapter((obj, member), IweixinapiMember)
            if api == None: return
            atnews = DexterityContainer(api,obj)
            data = {}
            try:
                followers = api.get_followers()['data']['openid']
            except:
                raise Exception("some error")        
            data["touser"] = followers
            data["mpnews"] = atnews.upload_news()
            data["msgtype"] = "mpnews"        
            api.send_by_openid(data)
    else:
        pass             
        