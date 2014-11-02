from zope.i18n import translate
from Products.validation import validation
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

#from my315ok.wechat.emailer import send_message

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
        form = self.request.form

        if 'form_submitted' in form:
            # The user clicked on the 'send by mail'
            # button.

            msg = _(u'msg_success',
                        default=u'The message has been sent')
            msg_type = 'info'


            self.context.plone_utils.addPortalMessage(
                translate(msg,
                          target_language=self.get_lang()),
                type=msg_type)


        elif 'form_cancelled' in form:
            # The user clicked on the 'cancel' button.
            self.request.response.redirect(self.context.absolute_url())

