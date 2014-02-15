# -*- coding: utf-8 -*-
"""Agent Profile Viewlet"""

#zope imports
from plone.app.layout.viewlets.common import ViewletBase
#from plone.app.layout.navigation.interfaces import INavigationRoot
#from plone.directives import form
from plone.memoize.view import memoize

from zope.interface import Interface, alsoProvides, noLongerProvides
from zope.traversing.browser.absoluteurl import absoluteURL

#local import
from customer.krainrealestate.browser.interfaces import IKrainViewlets
from customer.krainrealestate import _

CONFIGURATION_KEY = 'customer.krainrealestate.agentprofile'

class IPossibleAgentProfile(Interface):
    """Marker interface for possible HeaderPlugin viewlet."""

class IAgentProfile(IKrainViewlets):
    """Marker interface for HeaderPlugin viewlet."""


class AgentProfileViewlet(ViewletBase):
    """Show Header plugins."""

    @property
    def available(self):
        return IPossibleAgentProfile.providedBy(self.context) and \
            IAgentProfile.providedBy(self.context)

    def update(self):
        """Prepare view related data."""
        super(AgentProfileViewlet, self).update()

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'


class AgentProfileStatus(object):
    """Return activation/deactivation status of AgentProfile viewlet."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def can_activate(self):
        return IPossibleAgentProfile.providedBy(self.context) and \
            not IAgentProfile.providedBy(self.context)

    @property
    def active(self):
        return IAgentProfile.providedBy(self.context)


class AgentProfileToggle(object):
    """Toggle AgentProfile viewlet for the current context."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        msg_type = 'info'

        if IAgentProfile.providedBy(self.context):
            # Deactivate AgentProfile viewlet.
            noLongerProvides(self.context, IAgentProfile)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u"'AgentProfile' viewlet deactivated.")
        elif IPossibleAgentProfile.providedBy(self.context):
            alsoProvides(self.context, IAgentProfile)
            self.context.reindexObject(idxs=['object_provides', ])
            msg = _(u"'AgentProfile' viewlet activated.")
        else:
            msg = _(
                u"The 'AgentProfile' viewlet does't work with this content "
                u"type. Add 'IPossibleAgentProfile' to the provided "
                u"interfaces to enable this feature."
            )
            msg_type = 'error'

        self.context.plone_utils.addPortalMessage(msg, msg_type)
        self.request.response.redirect(self.context.absolute_url())