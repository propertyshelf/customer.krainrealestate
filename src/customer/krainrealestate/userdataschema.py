 # -*- coding: utf-8 -*-
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from customer.krainrealestate import _


areas_options = SimpleVocabulary([
    SimpleTerm(value='Alajuela', title=_(u'Alajuela')),
    SimpleTerm(value='Cartago', title=_(u'Cartago')),
    SimpleTerm(value='Guanacaste', title=_(u'Guanacaste')),
    SimpleTerm(value='Heredia', title=_(u'Heredia')),
    SimpleTerm(value='Lim\xf3n', title=_(u'Limón')),
    SimpleTerm(value='Puntarenas', title=_(u'Puntarenas')),
    SimpleTerm(value='San Jos\xe9', title=_(u'San José')),
    ])
languages_options = SimpleVocabulary([
    SimpleTerm(value='English', title=_(u'English')),
    SimpleTerm(value='Spanish', title=_(u'Español')),
    SimpleTerm(value='German', title=_(u'Deutsch')),
    SimpleTerm(value='French', title=_(u'Français')),
    SimpleTerm(value='Russian', title=_(u'русский')),
    SimpleTerm(value='Italian', title=_(u'Italiano')),
    SimpleTerm(value='Chinese', title=_(u'中国的')),
    ])

def validateAccept(value):
    if not value == True:
        return False
    return True

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    office_name = schema.TextLine(
        title=_(u'label_office_name', default=u'Name of your Office'),
        description=_(u'help_office_name',
                      default=u"Fill in the name of the Office your are working for."),
        required=False,
        )
    office_adress = schema.TextLine(
        title=_(u'label_office_adress', default=u'Office Adress'),
        description=_(u'help_office_adress',
                      default=u"Fill in the adress of your office."),
        required=False,
        )
    office_phone = schema.TextLine(
        title=_(u'label_office_phone', default=u'Office Phone'),
        description=_(u'help_office_phone',
                      default=u"Fill in your phone number in the office."),
        required=False,
        )
    us_line = schema.TextLine(
        title=_(u'label_us_line', default=u'U.S. Line'),
        description=_(u'help_us_line',
                      default=u"Fill in your U.S. Line phone nr."),
        required=False,
        )
    cell_phone = schema.TextLine(
        title=_(u'label_cell_phone', default=u'Cell Phone'),
        description=_(u'help_cell_phone',
                      default=u"Fill in your cell phone nr."),
        required=False,
        )
    skype_name = schema.TextLine(
        title=_(u'label_skype_name', default=u'Skype Name'),
        description=_(u'help_skype_name',
                      default=u"Fill in your Skype name"),
        required=False,
        )
    areas = schema.Choice(
        title=_(u'label_areas', default=u'Select the areas you service'),
        description=_(u'help_areas',
                      default=u"In which areas are you active?"),
        vocabulary = areas_options,
        required=False,
        )
    languages = schema.Choice(
        title=_(u'label_languages', default=u'Select the languages you speak.'),
        description=_(u'help_languages',
                      default=u"In which languages you can speak with customers?"),
        vocabulary = languages_options,
        required=False,
        )
    social_fb = schema.TextLine(
        title=_(u'label_facebook_name', default=u'Facebook Name'),
        description=_(u'help_facebook_name',
                      default=u"Fill in your Facebook name"),
        required=False,
        )
    social_twitter = schema.TextLine(
        title=_(u'label_twitter_name', default=u'Twitter Name'),
        description=_(u'help_twitter_name',
                      default=u"Fill in your twitter name"),
        required=False,
        )
    social_youtube = schema.TextLine(
        title=_(u'label_youtube_chanel', default=u'Youtube Chanel'),
        description=_(u'help_youtube_chanel',
                      default=u"Fill in your youtube chanel name"),
        required=False,
        )
    social_google = schema.TextLine(
        title=_(u'label_google_name', default=u'g+ Name'),
        description=_(u'help_youtube_chanel',
                      default=u"Fill in your google g+ name"),
        required=False,
        )
    social_Linkedin = schema.TextLine(
        title=_(u'label_linkedin_name', default=u'LinkedIn name'),
        description=_(u'help_youtube_chanel',
                      default=u"Fill in your LinkedIn account name"),
        required=False,
        )
