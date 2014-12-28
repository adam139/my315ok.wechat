# -*- coding: utf-8 -*-

import unittest


class TestBasic(unittest.TestCase):

    def _makeTwo(self):
        from dexterity.membrane.content.member import member
        dummy = member()
        import pdb
        pdb.set_trace()
        from my315ok.wechat.behaviors.wechat_token import WechatApiKey
        return WechatApiKey(dummy)        
    
    def _makeOne(self):
        class Dummy(object):
            pass
        dummy = Dummy()
        from my315ok.wechat.behaviors.wechat_token import WechatApiKey
        return WechatApiKey(dummy)

    def test_appid_setter2(self):
        b = self._makeTwo()
        b.appid = u'foo'
        self.assertEqual(u'foo', b.context.appid)

    def test_appid_setter(self):
        b = self._makeOne()
        b.appid = u'foo'
        self.assertEqual(u'foo', b.context.appid)

    def test_appid_setter_rejects_bytestrings(self):
        b = self._makeOne()
        self.assertRaises(ValueError, setattr, b, 'appid', 'føø')

    def test_appid_getter(self):
        b = self._makeOne()
        b.context.appid = u'foo'
        self.assertEqual(u'foo', b.appid)

    def test_appsecret_setter(self):
        b = self._makeOne()
        b.appsecret = u'foo'
        self.assertEqual(u'foo', b.context.appsecret)

    def test_appsecret_setter_rejects_bytestrings(self):
        b = self._makeOne()
        self.assertRaises(ValueError, setattr, b, 'appsecret', 'føø')

    def test_appsecret_getter(self):
        b = self._makeOne()
        b.context.appsecret = u'foo'
        self.assertEqual(u'foo', b.appsecret)


