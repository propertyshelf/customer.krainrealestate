# -*- coding: utf-8 -*-
"""Agent Search Viewlet"""

#zope imports
from Acquisition import aq_inner

from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface, alsoProvides, noLongerProvides

#local imports
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

class AgentProfileStatus(object):
    """Return activation/deactivation status of AgentProfile viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleAgentSearch.providedBy(self.context) and \
            not IAgentSearch.providedBy(self.context)

    @property
    def active(self):
        return IAgentSearch.providedBy(self.context)


class AgentSearchToggle(object):
    """Toggle AgentSearch viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IAgentSearch.providedBy(self.context):
            # Deactivate AgentProfile viewlet.
            noLongerProvides(self.context, IAgentSearch)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u"'AgentSearch' viewlet deactivated.")
        elif IPossibleAgentSearch.providedBy(self.context):
            alsoProvides(self.context, IAgentSearch)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u"'AgentSearch' viewlet activated.")
        else:
            msg = _(
                u"The 'AgentSearch' viewlet does't work with this content "
                u"type. Add 'IPossibleAgentProfile' to the provided "
                u"interfaces to enable this feature."
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())
