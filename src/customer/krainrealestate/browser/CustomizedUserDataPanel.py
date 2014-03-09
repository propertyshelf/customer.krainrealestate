from plone.app.users.browser.personalpreferences import UserDataPanel

class CustomizedUserDataPanel(UserDataPanel):
    """ Hide certain form fields in the UserDataPanel """
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('location', 'description','agent_profile_en', 'agent_profile_es', 'agent_profile_de')

    def _on_save(self, data):
        """ implementing plone.app.users.browser.interfaces._on_save function
            for custom event handling
        """
        from pprint import pprint
        pprint('User Data saved, hook is hooking!')
        pprint(data)