from five import grok
from plone.directives import dexterity, form
from plone.indexer import indexer
from zope import schema

from my315ok.wechat import MessageFactory as _

# Interface class; used to define content-type schema.
from my315ok.wechat.interfaces import IMessage, ITextMessage,IImageMessage,\
IVoiceMessage,ILinkMessage,IVideoMessage,ILocationMessage

 
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class TextMessage(dexterity.Item):
    grok.implements(ITextMessage)
    grok.provides(ITextMessage)
    
    # Add your class methods and properties here
class ImageMessage(dexterity.Item):
    grok.implements(IImageMessage)
    grok.provides(IImageMessage)
    
class LinkMessage(dexterity.Item):
    grok.implements(ILinkMessage)
    grok.provides(ILinkMessage)
    
class VoiceMessage(dexterity.Item):
    grok.implements(IVoiceMessage)
    grok.provides(IVoiceMessage)  
    
class VideoMessage(dexterity.Item):
    grok.implements(IVideoMessage)
    grok.provides(IVideoMessage) 
    
class LocationMessage(dexterity.Item):
    grok.implements(ILocationMessage)
    grok.provides(ILocationMessage)               


@indexer(IMessage)
def FromUserName(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``content`` index with the answer .
    """
#    context = aq_inner(context)
    return context.FromUserName
