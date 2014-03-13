# -*- coding: utf-8 -*-
"""Customized UserDataPanel- used for 'Agent' management """

from Acquisition import aq_inner
from plone.app.users.browser.personalpreferences import UserDataPanel
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter

from customer.krainrealestate.browser.agentprofile_viewlet import IAgentProfile
from customer.krainrealestate.browser.interfaces import IAgentFolder

try:
    from plone.mls.listing.interfaces import ILocalAgencyInfo
    ps_mls = True
except:
    ps_mls = False

from pprint import pprint

class CustomizedUserDataPanel(UserDataPanel):
    """ Hide certain form fields in the UserDataPanel """
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('location', 'description','agent_profile_en', 'agent_profile_es', 'agent_profile_de')

    
    def _on_save(self, data):
        """ implementing plone.app.users.browser.interfaces._on_save function
            for custom event handling
        """
        
        if len(self.userid):
            #if we have a userid, use this as agent
            membershiptool = getToolByName(aq_inner(self.context), 'portal_membership')
            agent = membershiptool.getMemberById(self.userid)
        else:
            portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
            agent = portal_state.member()
            self.userid = agent.id

        if agent.has_role('Agent'):
            #custom save action only for "Agent" group
            pprint('User Data saved, hook is hooking for: ' + self.userid)
            agent_folders = self._get_AgentProfileFolders()
            if len(agent_folders):
                self._update_AgentInfoPortlet_ProfilePage(agent_folders, data)

    def _update_AgentInfoPortlet_ProfilePage(self, folders, data):
        """Override Annotation for plone.mls.listing AgentInfo inside AgentProfilePages"""
        pprint(folders)
        pprint(data)
        pprint(self.userid)
        #get agents portrait/ avatar url
        membershiptool = getToolByName(aq_inner(self.context), 'portal_membership')
        avatar_url = membershiptool.getPersonalPortrait(id=self.userid).absolute_url()
       
        for folder in folders:
            if IAgentFolder.providedBy(folder) and ILocalAgencyInfo.providedBy(folder):
                pprint('update folder:')
                pprint(folder)
                
                mls_ano = IAnnotations(folder).get("plone.mls.listing.localagencyinfo", {})

                mls_ano['agency_name'] = 'Krain Real Estate'
                mls_ano['agent_name'] = data.get('fullname', u'')
                mls_ano['agent_office_phone'] = data.get('office_phone', u'')
                mls_ano['agent_cell_phone'] = data.get('cell_phone', u'')
                mls_ano['agent_email'] = data.get('email', u'')
                mls_ano['agent_avatar_url'] = avatar_url

           

    def _get_AgentProfileFolders(self):
        """get all the Agents Folders
            @return: list of Agent folders for given agent, empty list for invalid
        """
        agent_id = self.userid
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        #look for all Agentprofile pages
        allprofilepages = catalog(object_provides=IAgentProfile.__identifier__, Language="all")
        #check if they belong to our agent
        #my_pages = []
        my_parents = []

        for ppage in allprofilepages:
            pp_obj = ppage.getObject()
            #look in the annotations of the profile page and get the agent_id value or empty string
            pp_agent = IAnnotations(pp_obj).get("customer.krainrealestate.agentprofile", {}).get("agent_id", u'')
            
            if pp_agent == agent_id:
                #my_pages.append(pp_obj)
                #get parent folders
                my_parents.append(pp_obj.aq_parent)
        
        return my_parents
