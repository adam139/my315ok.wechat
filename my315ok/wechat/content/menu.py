from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field


from plone.app.textfield import RichText



from zope.component import getUtility
from zope.component.hooks import getSite
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.dexteritytextindexer.behavior import IDexterityTextIndexer

# Interface class; used to define content-type schema.

class IMenu(form.Schema):
    """
    A conference event
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(title=_(u"Title"))
    dexteritytextindexer.searchable('description')    
    description = schema.Text(title=_(u"Summary"), required=True)

    sponsor = schema.TextLine(title=_(u"Sponsor"))
    menu_type = schema.Choice(
        title=_(u"Conference Type"),
        vocabulary="collective.conference.vocabulary.conferencetype"
    )    
    province = schema.Choice(
        title=_(u"province"),
        vocabulary="dexterity.membrane.vocabulary.province"
    )  
    address = schema.TextLine(title=_(u"Address"))   
    form.widget(rooms='plone.z3cform.textlines.TextLinesFieldWidget')
    rooms = schema.List(
        title=_(u"Available Rooms"),
        value_type=schema.TextLine()
    )
    participants = schema.List(
        title=_(u"Participants list"),
        value_type=schema.TextLine()
    )  
    speakers = schema.List(
        title=_(u"speakers list"),
        value_type=schema.TextLine()
    )  
    
    form.omitted('participants','speakers')  
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Conference(dexterity.Container):
    grok.implements(IConference)
    grok.provides(IConference)
    
    # Add your class methods and properties here

    def getConference(self):
        site = getSite()
        parent = self
        while parent != site:
            if IConference.providedBy(parent):
                return parent
            parent = aq_parent(parent)
        return None

