# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_office_name(self):
        return unicode(str(self.context.getProperty('office_name', '')), 'utf-8')
    def set_office_name(self, value):
        return unicode(str(self.context.setMemberProperties({'office_name': value})), 'utf-8')
    office_name = property(get_office_name, set_office_name)

    def get_office_adress(self):
        return unicode(str(self.context.getProperty('office_adress', '')), 'utf-8')
    def set_office_adress(self, value):
        return unicode(str(self.context.setMemberProperties({'office_adress': value})), 'utf-8')
    office_adress = property(get_office_adress, set_office_adress)

    def get_office_phone(self):
        return self.context.getProperty('office_phone', '')
    def set_office_phone(self, value):
        return self.context.setMemberProperties({'office_phone': value})
    office_phone = property(get_office_phone, set_office_phone)

    def get_us_line(self):
        return self.context.getProperty('us_line', '')
    def set_us_line(self, value):
        return self.context.setMemberProperties({'us_line': value})
    us_line = property(get_us_line, set_us_line)

    def get_cell_phone(self):
        return self.context.getProperty('cell_phone', '')
    def set_cell_phone(self, value):
        return self.context.setMemberProperties({'cell_phone': value})
    cell_phone = property(get_cell_phone, set_cell_phone)

    def get_skype_name(self):
        return unicode(str(self.context.getProperty('skype_name', '')), 'utf-8')
    def set_skype_name(self, value):
        return unicode(str(self.context.setMemberProperties({'skype_name': value})), 'utf-8')
    skype_name = property(get_skype_name, set_skype_name)

    def get_areas(self):
        """Split memberdata area string into a list"""
        value = [] 
        areas = self.context.getProperty('areas', '')
        if areas: 
             value = areas.split(',') 
        return value

    def set_areas(self, value):
        """Join area-list into area-string for portal_memberdata"""
        area_string = ','.join(value) 
        return self.context.setMemberProperties({'areas': area_string})

    areas = property(get_areas, set_areas)

    def get_languages(self):
        """Split memberdata languages string into a list"""
        value = [] 
        lang = self.context.getProperty('languages', '')
        if lang: 
             value = lang.split(',') 
        return value
        
    def set_languages(self, value):
        lang_string = ','.join(value)
        return self.context.setMemberProperties({'languages': lang_string})
    languages = property(get_languages, set_languages)

    def get_social_fb(self):
        return self.context.getProperty('social_fb', '')
    def set_social_fb(self, value):
        return self.context.setMemberProperties({'social_fb': value})
    social_fb = property(get_social_fb, set_social_fb)

    def get_social_twitter(self):
        return self.context.getProperty('social_twitter', '')
    def set_social_twitter(self, value):
        return self.context.setMemberProperties({'social_twitter': value})
    social_twitter = property(get_social_twitter, set_social_twitter)

    def get_social_youtube(self):
        return self.context.getProperty('social_youtube', '')
    def set_social_youtube(self, value):
        return self.context.setMemberProperties({'social_youtube': value})
    social_youtube = property(get_social_youtube, set_social_youtube)

    def get_social_google(self):
        return self.context.getProperty('social_google', '')
    def set_social_google(self, value):
        return self.context.setMemberProperties({'social_google': value})
    social_google = property(get_social_google, set_social_google)

    def get_social_linkedin(self):
        return self.context.getProperty('social_linkedin', '')
    def set_social_linkedin(self, value):
        return self.context.setMemberProperties({'social_linkedin': value})
    social_linkedin = property(get_social_linkedin, set_social_linkedin)