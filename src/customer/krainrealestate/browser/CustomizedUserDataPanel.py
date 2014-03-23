# -*- coding: utf-8 -*-
"""Customized UserDataPanel- used for 'Agent' management """

from Acquisition import aq_inner
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides

#local imports
from customer.krainrealestate.browser.agentprofile_viewlet import IAgentProfile, IPossibleAgentProfile
from customer.krainrealestate.browser.interfaces import IAgentFolder

# try to import plone.mls.listing interfaces for ps specific functions
try:
    from plone.mls.listing.interfaces import (
        ILocalAgencyInfo,
        IPossibleLocalAgencyInfo,
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
        membershiptool = getToolByName(aq_inner(self.context), 'portal_membership')


        languages = ['en', 'es', 'de']
        agent_profile = {   'en': {'id':'personal-description', 'title':'Personal Description' }, 
                            'es': {'id':'perfil-inmobiliario', 'title':'Perfil del Inmobiliario' }, 
                            'de': {'id':'makler-profil', 'title':'Makler Profil' }
        }
        agent_featured_folders = {
                            'en': {'id':'featured-listings', 'title':'Featured Listings' },
                            'es': {'id':'propiedades-destacadas', 'title':'Propiedades Destacadas' }, 
                            'de': {'id':'besondere-immobilien', 'title':'Besondere Immobilien' }
        }

        agent_folders = {
                            'en': {'id':'agents', 'title':'Agents' },
                            'es': {'id':'inmobiliarios', 'title':'Inmobiliarios' }, 
                            'de': {'id':'makler', 'title':'Makler' }
        }
        agent_blog_folders = {
                            'en': {'id':'blog', 'title':'Blog' },
                            'es': {'id':'blog', 'title':'Blog' }, 
                            'de': {'id':'blog', 'title':'Blog' }
        }

        if len(self.userid):
            member = membershiptool.getMemberById(self.userid)
            member_fullname = member.getProperty("fullname", self.userid)

            for lang in languages:
                # get the different navigation roots             
                navRoot = portal.unrestrictedTraverse(lang)
                #check if basic setup is done already
                agent_folders_id = agent_folders[lang]['id']
                agent_folders_title = agent_folders[lang]['title']
                my_path = '/'.join(context.getPhysicalPath())
                my_path = my_path + '/' + lang + '/' + agent_folders_id

                foo = catalog(path={ "query": my_path}, Language="all")
                if len(foo)==0:
                    #create main agent folders            
                    try:
                        new_folder = navRoot.invokeFactory('Folder', agent_folders_id, title=agent_folders_title, path=my_path)
                        agent_root = getattr(navRoot, new_folder,None)
                        workflowTool.doActionFor(agent_root, "publish",comment="published by setup (customer.krainrealestate)")
                        self.context.plone_utils.addPortalMessage('"'+new_folder+'" added.' , 'info')
                        
                    except Exception:
                        print Exception

                agentRoot= portal.unrestrictedTraverse(lang + "/" + agent_folders_id)
                
                try:
                    #test if agent folder already exists
                    newAgentFolder = agentRoot.invokeFactory('Folder', self.userid, title=member_fullname, path=my_path + "/" + self.userid)
                    agent_home = getattr(agentRoot, newAgentFolder,None)
                    workflowTool.doActionFor(agent_home, "publish",comment="published by setup (customer.krainrealestate)")
                    self.context.plone_utils.addPortalMessage('"'+newAgentFolder+'" added & published.' , 'info')
                    created = True
                    # activate local agency Info
                    if IPossibleLocalAgencyInfo.providedBy(agent_home):
                        alsoProvides(agent_home, ILocalAgencyInfo)
                        agent_home.reindexObject(idxs=['object_provides', ])

                    #Todo: 
                    #   + permission to 'See' in folder, publish

                except Exception:
                    """Folders exist already"""
                    created = False
                    print 'Personal Agent folder already exist'

                if(created):
                    """"setup the missing folders and contents"""
                    myAgentRoot = portal.unrestrictedTraverse(lang + "/" + agent_folders_id + "/" + self.userid) 
                    #set 'Blog' folder
                    blog_id= agent_blog_folders[lang]['id']
                    blog_title= agent_blog_folders[lang]['title']
                    try:
                        newAgentBlogFolder = myAgentRoot.invokeFactory('Folder', blog_id, title=blog_title, path=my_path + "/" + self.userid +"/"+blog_id)
                        agent_blog = getattr(myAgentRoot, newAgentBlogFolder,None)
                        workflowTool.doActionFor(agent_blog, "publish",comment="published by setup (customer.krainrealestate)")
                        self.context.plone_utils.addPortalMessage('"'+newAgentBlogFolder+'" added & published.' , 'info')
                    except Exception, e:
                        """Folders exist already"""
                        print 'Blog folder exists already'
                        print e
                    #Todo: 
                    #   + permission to 'Add' in folder, publish
                    #   + content type restriction to 'news', 'image'


                    #set 'Featured Listings' folder
                    featured_id= agent_featured_folders[lang]['id']
                    featured_title= agent_featured_folders[lang]['title']
                    try:
                        newAgentFeaturedFolder = myAgentRoot.invokeFactory('Folder', featured_id, title=featured_title, path=my_path + "/" + self.userid +"/"+featured_id)
                        agent_featured = getattr(myAgentRoot, newAgentFeaturedFolder,None)
                        workflowTool.doActionFor(agent_featured, "publish",comment="published by setup (customer.krainrealestate)")
                        self.context.plone_utils.addPortalMessage('"'+newAgentFeaturedFolder+'" added & published.' , 'info')
                    except Exception, e:
                        """Folders exist already"""
                        print 'Featured folder exist already'
                        print e
                    #Todo: 
                    #   + Featured Listing Collection
                    #   + permission to 'Add' in folder, publish
                    #   + content type restriction to 'listing'
                  

                    #create Profile page
                    profile_id = agent_profile[lang]['id']
                    profile_title = agent_profile[lang]['title']

                    try:
                        profilePage = myAgentRoot.invokeFactory('Document', profile_id, title=profile_title, path=my_path + "/" + self.userid +"/"+profile_id)
                        ppage = getattr(myAgentRoot, profilePage,None)
                        workflowTool.doActionFor(ppage, "publish",comment="published by setup (customer.krainrealestate)")
                        self.context.plone_utils.addPortalMessage('"'+profilePage+'" added,published.' , 'info')
                        #activate AgentProfile Viewlet
                        self._activateAgentProfile(ppage, profilePage)
                        
                    except Exception, e:
                        """Profile page already exists"""
                        print 'Profile Page: exist already'
                        print e
                        
                    #Todo:
                    #   + set default view
                    #   + permission 'edit'


    def _activateAgentProfile(self,ppage, title='AgentProfilePage'):
        """ activate Agent Profile"""
        CONFIGURATION_KEY = "customer.krainrealestate.agentprofile"
        if IPossibleAgentProfile.providedBy(ppage):
            alsoProvides(ppage, IAgentProfile)
            ppage.reindexObject(idxs=['object_provides', ])
            self.context.plone_utils.addPortalMessage('"'+title+'" activated for Agent.', 'info')

            anno = IAnnotations(ppage)
            anno.get(CONFIGURATION_KEY, anno.setdefault(CONFIGURATION_KEY, {'agent_id':self.userid}))
          

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
