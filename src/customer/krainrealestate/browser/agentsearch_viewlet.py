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

    def __getAgentProfilePage(self, agent_id):
        """Find the language-dependend AgentProfilePage"""
        language = self.language()
        # "field" is the language depending form field in the memberdata
        if language =='en':
            field = "agent_profile_en"
        elif language =='es':
            field = "agent_profile_es"
        elif language =='de':
            field = "agent_profile_de"
        else:
            msg = _(
                u"Your Language is not supported yet. As fallback we will use the english version"
            )
            msg_type = 'info'
            self.context.plone_utils.addPortalMessage(msg, msg_type)
            field = "agent_profile_en"
            
        return '/en/agent/test'

    def AgentPortrait(self, agent_id):
        """get Agents Portrait"""
        return self.membership.getPersonalPortrait(id=agent_id)

    def ProfileUrl(self, agent_id):
        """get the URL to the Agents Profile Page"""
        return self.__getAgentProfilePage(agent_id)

    @property
    def getAllAgents(self):
        """Get all Plone users with the role Agent"""
        agent_dict ={}
        for member in self.membership.listMembers():
            if member.has_role('Agent'):
                agent_id = member.getUserName()
                agent_dict[agent_id]={}
                agent_dict[agent_id]['email'] = member.getProperty('email')
                agent_dict[agent_id]['areas'] = self.__wrapAreas(member.getProperty('areas'))
                agent_dict[agent_id]['fullname'] = member.getProperty('fullname')
           
        return agent_dict

    def __wrapAreas(self, areas):
        """wrap the areas for html display"""
        areas_list = areas.strip().split('\n')
        areas_html = ''
        for value in areas_list:
            areas_html = areas_html + '<span class="area-list-item">' + value +'</span>'
        
        return areas_html

    @property
    def language(self):
        """ Get the language of the context.
            @return: The two letter language code of the current content.
        """
        portal_state = self.context.unrestrictedTraverse("@@plone_portal_state")
        return aq_inner(self.context).Language() or portal_state.default_language()


class AgentSearchStatus(object):
    """Return activation/deactivation status of AgentSearch viewlet."""

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
