"""refer  the plone.app.discussion indexers indexes
"""
import unittest2 as unittest

import transaction
from zope import event

from datetime import datetime

from zope.component import createObject
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from my315ok.wechat.testing import INTEGRATION_TESTING

from my315ok.wechat.content.menu import istopmenu as indexers
from plone.indexer.delegate import DelegatingIndexerFactory
from my315ok.wechat.tests.test_api import setupbase

class CatalogSetupTest(setupbase):
    layer = INTEGRATION_TESTING    

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.wechat.content.menufolder', 'menufolder1',title="menufolder1")
        
        portal['menufolder1'].invokeFactory('my315ok.wechat.content.menu','menu1',
                                               title="xixi",
                                               menu_type="click",
                                               url="",
                                               istopmenu='1',
                                               key="rich text1")
        portal['menufolder1']['menu1'].invokeFactory('my315ok.wechat.content.menu','submenu1',
                                               title="submenu1-1",
                                               menu_type="click",
                                               url="",
                                               key="rich text1")
        portal['menufolder1']['menu1'].invokeFactory('my315ok.wechat.content.menu','submenu2',
                                               title="submenu1-2",
                                               menu_type="click",
                                               url="",
                                               key="rich text1")                
        portal['menufolder1'].invokeFactory('my315ok.wechat.content.menu','menu2',
                                               title="skip",
                                               menu_type="view",
                                               istopmenu="1",
                                               url="http://315ok.org/",
                                               key="rich text1")
                


        self.portal = portal    

    
    def test_catalog_installed(self):
        self.assertTrue('istopmenu' in
                        self.portal.portal_catalog.indexes())
          

    def test_conversation_total_comments(self):
        self.assertTrue(isinstance(indexers,DelegatingIndexerFactory))       
        p1 = self.portal['menufolder1']['menu1']
        import pdb
        pdb.set_trace()
        self.assertEqual(indexers(p1)(), '1')
     

    def test_catalogsearch(self):   
        catalog2 = getToolByName(self.portal, 'portal_catalog')     

        results2 = list(catalog2({'istopmenu': '1'}))
        self.assertEqual(len(results2), 2)
       
         
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
