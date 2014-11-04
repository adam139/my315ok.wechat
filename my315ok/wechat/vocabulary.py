# -*- coding: utf-8 -*-
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory

from my315ok.wechat import MessageFactory as _




# 定义微信自定义菜单点击响应后的动作类型
menu_type=[('click','click',_(u'click event')),
           ('view','view',_(u'view skip event')),
                        ]
menu_terms = [SimpleTerm(value, token, title) for value, token, title in menu_type ]

class MenuTypes(object):

    def __call__(self, context):
        return SimpleVocabulary(menu_terms)

grok.global_utility(MenuTypes, IVocabularyFactory,
        name="my315ok.wechat.vocabulary.menutype")

istopmenu=[('1','1',_(u'is top menu')),
           ('0','0',_(u'is not top menu')),
                        ]
istopmenu_terms = [SimpleTerm(value, token, title) for value, token, title in istopmenu ]

class IsTopMenu(object):

    def __call__(self, context):
        return SimpleVocabulary(istopmenu_terms)

grok.global_utility(IsTopMenu, IVocabularyFactory,
        name="my315ok.wechat.vocabulary.istopmenu")
