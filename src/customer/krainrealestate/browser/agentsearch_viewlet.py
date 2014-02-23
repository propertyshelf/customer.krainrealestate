# -*- coding: utf-8 -*-
"""Agent Search Viewlet"""

#zope imports
from Acquisition import aq_inner


from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface


#local import
from customer.krainrealestate.browser.interfaces import IKrainViewlets
from customer.krainrealestate import _

CONFIGURATION_KEY = 'customer.krainrealestate.agentsearch'

class IPossibleAgentSearch(Interface):
    """Marker interface for possible HeaderPlugin viewlet."""

class IAgentSearch(IKrainViewlets):
    """Marker interface for HeaderPlugin viewlet."""


class AgentSearchViewlet(ViewletBase):
    """Show Header plugins."""

    @property
    def available(self):
        return IPossibleAgentSearch.providedBy(self.context) and \
            IAgentSearch.providedBy(self.context)

    def update(self):
        """Prepare view related data."""
        super(AgentSearchViewlet, self).update()

        context = aq_inner(self.context)
        self.membership = getToolByName(context, 'portal_membership')
