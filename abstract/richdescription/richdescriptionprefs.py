from zope.interface import Interface, implements
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter

from zope.formlib import form
from zope import schema
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator

from Products.statusmessages.interfaces import IStatusMessage
from plone.protect import CheckAuthenticator
from zope.event import notify
from plone.app.controlpanel.events import ConfigurationChangedEvent

from Products.CMFPlone import PloneMessageFactory as _p
from abstract.richdescription import MessageFactory as _


class IRichDescriptionForm(Interface):
    """ The view for RichDescription  prefs form. """

    allowed_types = schema.Tuple(title=_(u'Portal types'),
          description=_(u'Portal types lead image may be attached to.'),
          missing_value=tuple(),
          value_type=schema.Choice(
                   vocabulary="plone.app.vocabularies.UserFriendlyTypes"),
          required=False)


class RichDescriptionControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(IRichDescriptionForm)

    def __init__(self, context):
        super(RichDescriptionControlPanelAdapter, self).__init__(context)
        pprop = getUtility(IPropertiesTool)
        self.richdescription_properties = getattr(pprop,
                                'richdescription_properties', None)
        self.context = context

    def get_allowed_types(self):
        return self.richdescription_properties.allowed_types

    def set_allowed_types(self, allowed_types):
        self.richdescription_properties.allowed_types = allowed_types

    allowed_types = property(get_allowed_types, set_allowed_types)


class RichDescriptionForm(ControlPanelForm):
    """ The view class for the rich description preferences form. """

    implements(IRichDescriptionForm)
    form_fields = form.FormFields(IRichDescriptionForm)

    label = _(u'Rich Description Settings Form')
    description = _(u'Select properties for Rich Description')
    form_name = _(u'Rich Description Settings')

    @form.action(_p(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _p("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _p("No changes made.")

    @form.action(_p(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_p("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''
