# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_office_name(self):
        return self.context.getProperty('office_name', '')
    def set_office_name(self, value):
        return self.context.setMemberProperties({'office_name': value})
    office_name = property(get_office_name, set_office_name)

    def get_office_adress(self):
        return self.context.getProperty('office_adress', '')
    def set_office_adress(self, value):
        return self.context.setMemberProperties({'office_adress': value})
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
        return self.context.getProperty('skype_name', '')
    def set_skype_name(self, value):
        return self.context.setMemberProperties({'skype_name': value})
    skype_name = property(get_skype_name, set_skype_name)

    def get_areas(self):
        return self.context.getProperty('areas', '')
    def set_areas(self, value):
        return self.context.setMemberProperties({'areas': value})
    areas = property(get_areas, set_areas)

    def get_languages(self):
        return self.context.getProperty('languages', '')
    def set_languages(self, value):
        return self.context.setMemberProperties({'languages': value})
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