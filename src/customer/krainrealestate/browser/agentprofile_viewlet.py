# -*- coding: utf-8 -*-
"""Agent Profile Viewlet"""

#zope imports
from Acquisition import aq_inner

from urlparse import urlparse

from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName

from z3c.form import form,field, button
from zope import schema
from zope.annotation.interfaces import IAnnotations
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

        annotations = IAnnotations(self.context)
        config = annotations.get(CONFIGURATION_KEY, {})
        context = aq_inner(self.context)
        self.membership = getToolByName(context, 'portal_membership')

        self.agentId = config.get('agent_id', u'')
        self.agent = self.membership.getMemberById(self.agentId)
        try:
            self.proptool = self.agent.getProperty
        except AttributeError:
            """ No valid agent found """
            self.agent = None
            self.proptool = None
        

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'

    def safeLink(self, url, absolute=True):
        """check url string for evilness and give a False for empty strings or suspicios protocols"""
        link = urlparse(url)

        if len(link.netloc)==0 and len(link.path)==0:
            return False
        if len(link.scheme)==0:
                return 'http://' + link.geturl();
        if (link.scheme=='http' or link.scheme=='https'):
                return link.geturl()
        else:
            return False


    @property
    def get_AgentId(self):
        """Get Agent ID"""
        return self.agentId

    @property
    def get_Agent(self):
        """Get the Agent and its data"""
        return self.agent

    @property
    def AgentAvailable(self):
        """Agent Data available?"""
        if (self.agent is not None):
            return True
        else:
            return False

    @property
    def Title(self):
        """Agent Fullname"""
        return self.proptool('fullname')

    @property
    def OfficeAvailable(self):
        """Office Data available?"""
        if (len(self.OfficeName)>0 or len(self.OfficeAdress)>0):
            return True
        else:
            return False

    @property
    def OfficeName(self):
        """"Delivers the name of the agents office"""
        return self.proptool('office_name')

    @property
    def OfficeAdress(self):
        """"Delivers the adress of the agents office"""
        return self.proptool('office_adress')

    @property
    def AgentContactAvailable(self):
        """Agent Contact Info available?"""
        return True

    @property
    def OfficePhone(self):
        """Return Agents office phone or False """
        value = self.proptool('office_phone')
        if len(value)>1:
            return value
        else:
            return False

    @property
    def USLine(self):
        """Return Agents 'US Line' or False """
        value = self.proptool('us_line')
        if len(value)>1:
            return value
        else:
            return False

    @property
    def CellPhone(self):
        """Return Agents cell phone nr. or False """
        value = self.proptool('cell_phone')
        if len(value)>1:
            return value
        else:
            return False

    @property
    def SkypeName(self):
        """Return Agents skype name or False """
        value = self.proptool('skype_name')
        if len(value)>1:
            return value
        else:
         return False

    @property
    def Website(self):
        """Return Agents website or False """
        try:
            return self.safeLink(self.proptool('home_page')) 
        except:
            return False

    @property
    def AgentEmail(self):
        """Returns a mailto Link to the Agent or False """
        value = self.proptool('email')
        if len(value)>1:
            return value
        else:
            return False

    @property
    def AgentLanguagesAvailable(self):
        """Languages available?"""
        if(len(self.proptool('languages'))>0):
            return True
        else:
            return False

    @property
    def Languages(self):
        """"Deliver Languages of the Agent"""
        return self.proptool('languages')

    @property
    def AgentSocialAvailable(self):
        """Agent Social Sharing Info available?"""
        return False

    @property
    def AgentPortraitAvailable(self):
        """Agent Portrait available?"""
        if (self.agent is not None):
            return True
        else:
            return False

    @property
    def AgentPortrait(self):
        """get the agents portrait"""
        try:
            return self.membership.getPersonalPortrait(id=self.agentId)
        except:
            return False
    

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

class IAgentProfileConfiguration(Interface):
    """AgentProfile Configuration Form."""

    agent_id = schema.TextLine(
        required=True,
        title=_(
            u'Agent ID',
            default=u'Please enter the Plone Member ID of the Agent',
        ),
    )


class AgentProfileConfiguration(form.Form):
    """AgentProfile Configuration Form."""

    fields = field.Fields(IAgentProfileConfiguration)
    label = _(u"change 'Agent Profile'")
    description = _(
        u"Adjust the AgentProfile ID of this Page."
    )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations.get(CONFIGURATION_KEY,
                               annotations.setdefault(CONFIGURATION_KEY, {}))

    @button.buttonAndHandler(_(u'Save'))
    def handle_save(self, action):
        data, errors = self.extractData()
        if not errors:
            annotations = IAnnotations(self.context)
            annotations[CONFIGURATION_KEY] = data
            self.request.response.redirect(absoluteURL(self.context,
                                                       self.request))

    @button.buttonAndHandler(_(u'Cancel'))
    def handle_cancel(self, action):
        self.request.response.redirect(absoluteURL(self.context, self.request))
