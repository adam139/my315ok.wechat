from five import grok
from plone.directives import dexterity, form
from plone.indexer import indexer
from zope import schema
from Products.CMFCore.utils import getToolByName

from my315ok.wechat import MessageFactory as _

from zope.component import getUtility
from zope.component.hooks import getSite
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.dexteritytextindexer.behavior import IDexterityTextIndexer

# Interface class; used to define content-type schema.

class IMenu(form.Schema):
    """
    A menu
    """
#    dexteritytextindexer.searchable('title')
#    title = schema.TextLine(title=_(u"Name"))

    menu_type = schema.Choice(
        title=_(u"menu type"),
        vocabulary="my315ok.wechat.vocabulary.menutype"
    )    
    istopmenu = schema.Choice(
        title=_(u"is top menu?"),
        vocabulary="my315ok.wechat.vocabulary.istopmenu",
        default='0'
    )      
    key = schema.TextLine(title=_(u"key value of the menu"))
 
    url = schema.TextLine(title=_(u"the menu link to url"))
       

    
#    form.omitted('description')  
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Menu(dexterity.Container):
    grok.implements(IMenu)
    grok.provides(IMenu)
    
    # Add your class methods and properties here



@indexer(IMenu)
def istopmenu(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``content`` index with the answer .
    """
#    context = aq_inner(context)
    return context.istopmenu
