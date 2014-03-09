# -*- coding: utf-8 -*-
"""Customized UserDataPanel- used for 'Agent' management """

from Acquisition import aq_inner
from plone.app.users.browser.personalpreferences import UserDataPanel
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations

from customer.krainrealestate.browser.agentprofile_viewlet import IAgentProfile

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

        membershiptool = getToolByName(aq_inner(self.context), 'portal_membership')
        agent = membershiptool.getMemberById(self.userid)

        if agent.has_role('Agent'):
            #custom save action only for "Agent" group
            pprint('User Data saved, hook is hooking for: ' + self.userid)
            agent_folders = self._get_AgentProfileFolders()
            pprint(agent_folders) 
            if len(agent_folders):
                self._update_AgentInfoPortlet_ProfilePage(agent_folders, data)

    def _update_AgentInfoPortlet_ProfilePage(self, folders, data):
        """Override Annotation for plone.mls.listing AgentInfo inside AgentProfilePages"""
        pprint(folders)
        pprint(data)
        

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
