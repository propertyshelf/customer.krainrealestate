# -*- coding: utf-8 -*-
"""Customized UserDataPanel- used for 'Agent' management """

from Acquisition import aq_inner
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter, getUtility

#local imports
from customer.krainrealestate.browser.agentprofile_viewlet import IAgentProfile
from customer.krainrealestate.browser.interfaces import IAgentFolder

# try to import plone.mls.listing interfaces for ps specific functions
try:
    from plone.mls.listing.interfaces import (
        ILocalAgencyInfo,
        IMLSAgencyContactInformation,
    )
    ps_mls = True
except:
    ps_mls = False


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
            #otherwise use logged in user 
            portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
            agent = portal_state.member()
            self.userid = agent.id

        if ps_mls and agent.has_role('Agent'):
            #custom save action only for "Agent" group
            agent_folders = self._get_AgentProfileFolders
            if len(agent_folders):
                self._update_AgentInfoPortlet_ProfilePage(agent_folders, data)
            else:
                #we don't have any AgentProfiles, so its time for basic setup
                self._basicAgentPagesSetup

    def _update_AgentInfoPortlet_ProfilePage(self, folders, data):
        """Override Annotation for plone.mls.listing AgentInfo inside AgentProfilePages"""
        #get agents portrait/ avatar url
        membershiptool = getToolByName(aq_inner(self.context), 'portal_membership')
        avatar_url = membershiptool.getPersonalPortrait(id=self.userid).absolute_url()
        #get AgencyInfo
        agency = self.__AgencyInfo
       
        for folder in folders:
            if IAgentFolder.providedBy(folder) and ILocalAgencyInfo.providedBy(folder):
                #get annotations for this folder
                mls_ano = IAnnotations(folder).get("plone.mls.listing.localagencyinfo", {})
                # set global Agency Info
                mls_ano['agency_name'] = agency.get('agency_name', u'Krain Real Estate')
                mls_ano['agency_logo_url'] = agency.get('agency_logo_url', u'')
                mls_ano['agency_office_phone'] = agency.get('agency_office_phone', u'')
                mls_ano['agency_website'] = agency.get('agency_website', u'')
                
                #Agent Info
                mls_ano['agent_name'] = data.get('fullname', u'')
                mls_ano['agent_office_phone'] = data.get('office_phone', u'')
                mls_ano['agent_cell_phone'] = data.get('cell_phone', u'')
                mls_ano['agent_email'] = data.get('email', u'')
                mls_ano['agent_avatar_url'] = avatar_url

                #force overrding of Any other agent
                mls_ano['force'] = 'selected'

    @property
    def _basicAgentPagesSetup(self):
        """setup basic agent folder structure """
        context = self.context
        portal = aq_inner(self.context)
        catalog = getToolByName(portal, 'portal_catalog')
        workflowTool = getToolByName(portal, "portal_workflow")


        languages = ['en', 'es', 'de']
        agent_folders = {'en':'agents', 'es': 'inmobiliarios', 'de':'makler'}
        agent_profile = {'en': 'Personal Description', 'es': 'Perfil del Agente', 'de':'Makler Profil'}
        agent_featured = {'en':'Featured Listings', 'es': 'Propiedades Destacadas', 'de':'Meine Immobilien'}

        if len(self.userid):         
            for lang in languages:
                # get the different navigation roots             
                navRoot = portal.unrestrictedTraverse(lang)
                #check if basic setup is done already
                
                my_path = '/'.join(context.getPhysicalPath())
                my_path = my_path + '/' + lang + '/' + agent_folders[lang]

                foo = catalog(path={ "query": my_path}, Language="all")
                if len(foo)==0:
                    #create folder            
                    try:
                        new_folder = navRoot.invokeFactory('Folder', agent_folders[lang], title=agent_folders[lang], path=my_path)
                        bar = getattr(navRoot, new_folder,None)
                        workflowTool.doActionFor(bar, "publish",comment="published by setup (customer.krainrealestate)")

                    except:
                        pass

    @property
    def __AgencyInfo(self):
        """Get global Agency Info from Config"""
        settings = {}
        registry = getUtility(IRegistry)
    
        if registry is not None:
            try:
                registry_settings = registry.forInterface(IMLSAgencyContactInformation)
            except:
                print('Global agency information not available.')
            else:
                settings = dict([
                    (a, getattr(registry_settings, a)) for a in
                    registry_settings.__schema__]
                )
        return settings
           
    @property
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
