#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.wechat import MessageFactory as _

from my315ok.wechat.content.menu import IMenu
from my315ok.wechat.content.menufolder import IMenufolder


from plone.memoize.instance import memoize

from Products.CMFCore import permissions
grok.templatedir('templates') 

class MenufolderView(grok.View):
    grok.context(IMenufolder)
    grok.template('menu_folder')
    grok.name('view')
    grok.require('zope2.View')    
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm 
       
    @memoize    
    def getHomeFolder(self):
        member = self.pm().getAuthenticatedMember()
        member_id = member.getId()
        member_folder = self.pm().getHomeFolder(member_id)
        return member_folder 
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ModifyPortalContent,self.context) 

    @memoize         
    def getMenuFolder(self):

        topicfolder = self.catalog()({'object_provides': IMenufolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath  

        
    @memoize         
    def get_top_menu(self):

        context = aq_inner(self.context)

        sepath= '/'.join(self.context.getPhysicalPath())
         
        topmenus = self.catalog()({'object_provides': IMenu.__identifier__,'istopmenu':'1','path':sepath})
           
        return topmenus
    
    def get_sub_menu(self,brain):
        """获取二级menu
        brain:topmenu item's brain
        """
#        import pdb
#        pdb.set_trace()
        sepath = brain.getPath()
        submenus = self.catalog()({'object_provides': IMenu.__identifier__,'istopmenu':'0','path':sepath})
           
        return submenus        
        
        
    def isexist_submenu(self,brain):
        """current menu is exist submenu
        """
        menus = self.get_sub_menu(brain)
        return bool(menus)
        
        
    def out_menus(self):
        """
    <div class="btn-group">
              <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown">
    Dropdown
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Action</a></li>
    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Another action</a></li>
    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Something else here</a></li>
    <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Separated link</a></li>
  </ul>
</div>    
        """
        output = ''

        for i in self.get_top_menu():            
            head="""<div class="row"><div class="col-xs-4 btn-group">"""
            tail = """</ul></div></div>"""
            if self.isexist_submenu(i):                
                top = """<button class="btn dropdown-toggle" type="button" data-toggle="dropdown">
            %s<span class="caret"></span>
            </button><ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">""" % i.Title
                subout = ""
                for sub in self.get_sub_menu(i):
                    submenu="""<li role="presentation"><a role="menuitem" tabindex="-1" href="%s">%s</a></li>""" % (sub.getURL(),sub.Title)
                    subout= subout + submenu
                
                submenu = subout + tail
                out = head + top + submenu            
            else:
                tail = """</div>"""
                top = """<button class="btn" type="button"><a href="%s">%s</a></button>""" % (i.getURL(),i.Title)
                out = head + top + tail
            output = output + out
#        import pdb
#        pdb.set_trace()
        return output
                
            

                
                    
        
             