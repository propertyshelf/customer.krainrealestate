# -*- coding: utf-8 -*-
import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from customer.krainrealestate.testing import\
    CUSTOMER_KRAINREALESTATE_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = CUSTOMER_KRAINREALESTATE_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
    
    def test_product_is_installed(self):
        """Test that the product is installed."""
        self.assertTrue(self.qi_tool.isProductInstalled(
            'customer.krainrealestate'))
