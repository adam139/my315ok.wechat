#-*- coding: UTF-8 -*-
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from my315ok.wechat import MessageFactory as _
from my315ok.wechat.browser.base import BaseView


class SendForm(BaseView):
    """ If the user does not have Javascript enabled, he is
    redirected to this page.
    This page generates the PDF using the URL of the previous page
    and shows a form to send it by mail.

    It should logically show the same thing than the previous page
    (the user has no JS enabled so no funky stuff happened).
    The only case it could fail is if the previous page was processing a
    POST form. In this case, we can just render the page as if it was
    called with a simple GET request.
    """

    def __call__(self):

        self.index = ZopeTwoPageTemplateFile('templates/send_page.pt')
            # We need the self parameter for Plone 4
        return self.index(self)
