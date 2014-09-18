# -*- coding: utf-8 -*-
import zope.interface 

class IMessage(zope.interface.Interface):
    """
    以微信服务器和开发平台之间双向传送的xml形式的消息报文的基本报文格式
    """
    ToUserName = zope.interface.Attribute("""接收该消息的收件人，或者是公众平台账号，或者微信用户账号""")
    FromUserName = zope.interface.Attribute("""发送该消息的发件人，或者是公众平台账号，或者微信用户账号""")
    CreatedTime = zope.interface.Attribute("""消息的创建时间，整型""")
    MsgType = zope.interface.Attribute("""该消息的类型，支持:text,image,voice,video,location,link""")
    MsgId = zope.interface.Attribute("""消息id，64位整型 """)
  
class IVoiceMessage(IMessage):
    """
    语音类型消息    
    """
    Content = zope.interface.Attribute("""文本消息内容""") 
    
class IImageMessage(IMessage):
    """
    图片类型消息    
    """       
    PicUrl = zope.interface.Attribute("""图片链接""") 
    MediaId = zope.interface.Attribute("""图片消息媒体id，可以调用多媒体文件下载接口拉取数据""")   
    
class IVocieMessage(IMessage):
    """
    图片类型消息    
    """       
    Format = zope.interface.Attribute("""语音格式，如amr，speex等""")     
    MediaId = zope.interface.Attribute("""语音消息媒体id，可以调用多媒体文件下载接口拉取数据""")  
    
class IVideoMessage(IMessage):
    """
    视频类型消息    
    """       
    ThumbMediaId = zope.interface.Attribute("""视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据""")     
    MediaId = zope.interface.Attribute("""视频消息媒体id，可以调用多媒体文件下载接口拉取数据""") 
    
class ILocationMessage(IMessage):
    """
    地理位置类型消息    
    """       
    Location_X = zope.interface.Attribute("""地理位置维度""")   
    Location_y = zope.interface.Attribute("""地理位置经度""")
    Scale = zope.interface.Attribute("""地图缩放大小""")              
    Label = zope.interface.Attribute("""地理位置信息""") 
    
class ILinkMessage(IMessage):
    """
    链接类型消息    
    """       
    Title = zope.interface.Attribute("""消息标题""")   
    Description = zope.interface.Attribute("""消息描述""")    
    Url = zope.interface.Attribute("""消息链接""")     
    
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
    
        
                 