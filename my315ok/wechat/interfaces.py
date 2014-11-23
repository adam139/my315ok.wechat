# -*- coding: utf-8 -*-
import zope.interface 
from zope import schema
from plone.directives import form
from my315ok.wechat import MessageFactory as _

class IMessage(form.Schema):
    """
    以微信服务器和开发平台之间双向传送的xml形式的消息报文的基本报文格式
    """
    ToUserName = schema.TextLine(title=_(u"the user name of receive message")) ##"""接收该消息的收件人，或者是公众平台账号，或者微信用户账号"""
    FromUserName = schema.TextLine(title=_(u"the user name of send message")) ##"""发送该消息的发件人，或者是公众平台账号，或者微信用户账号"""
    CreatedTime = schema.Int(title=_(u"time of created message")) ##"""消息的创建时间，整型"""
    MsgType = schema.TextLine(title=_(u"type of message")) ##"""该消息的类型，支持:text,image,voice,video,location,link"""
    MsgId = schema.ASCIILine(title=_(u"Id of message"))   ##"""消息id，64位整型 """

  
class ITextMessage(IMessage):
    """
    语音类型消息    
    """
    Content = schema.Text(title=_(u"content of message"))   ##"""文本消息内容"""
    
class IImageMessage(IMessage):
    """
    图片类型消息    
    """       
    PicUrl = schema.URI(title=_(u"URL of the image message link to"))   ##"""图片链接"""
    MediaId = schema.Id(title=_(u"media id of the image message"))   ##"""图片消息媒体id，可以调用多媒体文件下载接口拉取数据""" 
    
class IVoiceMessage(IMessage):
    """
    图片类型消息    
    """       
    Format = schema.TextLine(title=_(u"format of the voice message"))   ##"""语音格式，如amr，speex等"""   
    MediaId = schema.Id(title=_(u"media id of the voice message"))   ##"""语音消息媒体id，可以调用多媒体文件下载接口拉取数据"""
    
class IVideoMessage(IMessage):
    """
    视频类型消息    
    """       
    ThumbMediaId = schema.Id(title=_(u"thumb media id of the video message"))   ##"""视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据"""   
    MediaId = schema.Id(title=_(u"media id of the video message"))   ##"""视频消息媒体id，可以调用多媒体文件下载接口拉取数据"""
    
class ILocationMessage(IMessage):
    """
    地理位置类型消息    
    """       
    Location_X = schema.Float(title=_(u" latitude of the location message"))   ##"""地理位置纬度""" 
    Location_y = schema.Float(title=_(u"longitude of the location message"))   ##"""地理位置经度"""
    Scale = schema.Int(title=_(u"Location accuracy of the location message"))   ##"""地图缩放大小"""            
    Label = schema.TextLine(title=_(u"label  of the location message"))   ##"""地理位置信息"""
    
class ILinkMessage(IMessage):
    """
    链接类型消息    
    """       
    Title = schema.TextLine(title=_(u"title of the link message"))   ##"""消息标题""" 
    Description = schema.TextLine(title=_(u"description of the link message"))   ##"""消息描述"""  
    Url = schema.URI(title=_(u"URL of the link message"))   ##"""消息链接"""   
    
class IAnalyzeMessage(zope.interface.Interface):
    """
    分析从微信服务器过来的xml报文,根据报文类型MsgType，实例化该报文
    """ 
    
    def xml_to_dic(xml):
        """
        xml为来自微信服务器原始报文，解析该xml文档，返回一个字典结构，
        该字典结构新增两个键值，一个为raw,一个为type
        """
    def create_message(messagedic):
            """
       xml根据解析结果，构建报文实例，
            该实例为TextMessage,PictureMessage等其中之一的一个实例。
            根据报文类型，构建正确的报文类名。如报文类型(MsgType)为text,则对应
            的类名为TextMessage; capitalize()?
            """  
class ICheckSignature(zope.interface.Interface):
    """
    加密/校验流程如下：
1. 将token、timestamp、nonce三个参数进行字典序排序
2. 将三个参数字符串拼接成一个字符串进行sha1加密
3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信

    """ 
    def __call__(token,timestamp,nonce,signature): 
            """
            加密/校验流程如下：
1. 将token、timestamp、nonce三个参数进行字典序排序
2. 将三个参数字符串拼接成一个字符串进行sha1加密
3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信

            """   
class Iweixinapi(zope.interface.Interface):
    """
    api marker interface
    """    
        
class IwechatSettings(zope.interface.Interface):
    """Describes registry records
    """
    
    appid = schema.ASCII(
            title=_(u"app id"),
            description=_(u"weixin app id"),
        )
    appsecret = schema.ASCII(
                             title=_(u"app secret"),
                             description=_(u"weixin app secret"),
                             )
    token = schema.ASCII(
                             title=_(u"app token"),
                             description=_(u"weixin app token"),
                             )    
    
class ISendWechatEvent(zope.interface.Interface):
    """
    a send wechat event mark interface.
    """  
class IReceiveWechatEvent(zope.interface.Interface):
    """
    a receive wechat event mark interface.
    """        
                     