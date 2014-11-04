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


class AjaxSend(grok.View):
    """AJAX action: send current to weixin.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax_send_weixin')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        id = data['id']
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'object_provides': IATNewsItem.__identifier__,
                                  'id': id})
        data = {'info':1}
        event.notify(SendWechatEvent(brains[0].getObject()))
        return json.dumps(data)
    
class AjaxCreate(grok.View):
    """AJAX action: send current to weixin.
    """
    
    grok.context(IMenufolder)
    grok.name('ajax_create_menu')
    grok.require('zope2.View')
        
    def render(self):
        # get menufolder view
        mview = getMultiAdapter((self.context, self.request),name=u"view") 
        data = self.request.form
        id = data['id']
        topmenu = mview.get_top_menu()
        if len(topmenu) == 0:
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
            
        else:
            menu_data = {"button":[]}
            
        for bn in topmenu:
            topitem = {}
            if mview.isexist_submenu(bn):
                topitem['name'] = bn.Title
                topitem['sub_button'] =[]
                for bn2 in mview.get_sub_menu(bn):
                    subitem = {}
                    obj = bn2.getObject()
                    subitem['name'] = bn2.Title
                    subitem['type'] = obj.menu_type
                    subitem['key'] = obj.key
                    subitem['url'] = obj.url
                    topitem['sub_button'].append(subitem)
                    
            else:
                obj = bn.getObject()
                topitem['name'] = bn.Title
                topitem['type'] = obj.menu_type
                topitem['key'] = obj.key
                topitem['url'] = obj.url
                
            menu_data['button'].append(topitem)
            
        catalog = getToolByName(self.context, 'portal_catalog')
        import pdb
        pdb.set_trace()
        # get a menu item
        brains = catalog({'object_provides': IATNewsItem.__identifier__,
                                  'limit': 1})
        menu = brains[0].getObject()
        # get wechat api adapter
        api = Iweixinapi(menu)
        try:
            mdata = api.get_menu()
          #has old menu
            rc = check_error(api.delete_menu())
            if rc['errcode'] == 0:
                rc = check_error(api.create_menu(menu_data))
        except:   #has not old menu
            rc = check_error(api.create_menu(menu_data))
                
        
        data = {'info':rc['errcode']}

        return json.dumps(data)    
         