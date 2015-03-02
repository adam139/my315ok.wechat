import os
from datetime import datetime
from random import randint

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize



class BaseView(BrowserView):
    """ Class used to factorize some code for the different views
    used in the product.
    """
    error_mapping = {}

    def __init__(self, *args, **kwargs):
        """ We just need to define some instance variables.
        """
        super(BaseView, self).__init__(*args, **kwargs)

        # The list of errors found when checking the form.
        self.errors = []

    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm

    @property
    def isEditable(self):
        from Products.CMFCore.permissions import ModifyPortalContent
        return self.pm().checkPermission(ModifyPortalContent,self.context)

    def get_lang(self):
        """ Finds the language to use.
        """
        props = getToolByName(self.context,
                              'portal_properties')
        return props.site_properties.getProperty('default_language') or 'en'

    def get_user(self):
        """ Returns the currently logged-in user.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            return

        return mtool.getAuthenticatedMember()

    def get_user_fullname(self):
        """ Returns the currently logged-in user's fullname.
        """
        member = self.get_user()
        if member:
            return member.getProperty('fullname')

    def get_user_email(self):
        """ Returns the currently logged-in user's email.
        """
        member = self.get_user()
        if member:
            return member.getProperty('email')


