# -*- coding: utf-8 -*-

import imp

class WxPayConf_pub(object):
    """配置账号信息"""

    #=======【基本信息设置】=====================================
    #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID = "ni6cfbaijkl9b9caf3"
    #JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
    APPSECRET = "****1a55****67ffe3d5e60fd9739724"
    #接口配置token
    TOKEN = "brain"
    #受理商ID，身份标识
    MCHID = "****27****"
    #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY = "********************************"
   

    #=======【异步通知url设置】===================================
    #异步通知url，商户根据实际开发过程设定
    NOTIFY_URL = "http://weixin.315ok.com/payback"

    #=======【证书路径设置】=====================================
    #证书路径,注意应该填写绝对路径
    SSLCERT_PATH = "/home/plone/cacert/apiclient_cert.pem"
    SSLKEY_PATH = "/home/plone/cacert/apiclient_key.pem"

    #=======【curl超时设置】===================================
    CURL_TIMEOUT = 30

    #=======【HTTP客户端设置】===================================
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL", "REQUESTS")

class ConfigAttribute(object):
    """
    让一个属性指向一个配置
    """

    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def from_pyfile(self, filename):
        """
        在一个 Python 文件中读取配置。

        :param filename: 配置文件的文件名。
        """
        d = imp.new_module('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec (compile(config_file.read(), filename, 'exec'), d.__dict__)
        self.from_object(d)
        return True

    def from_object(self, obj):
        """
        在给定的 Python 对象中读取配置。

        :param obj: 一个 Python 对象
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
