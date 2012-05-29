# -*- coding: utf-8 -*-

from zope.component import adapts, getUtility
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf

from archetypes.schemaextender.interfaces import (IBrowserLayerAwareExtender,
                                                IOrderableSchemaExtender)
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.field import ExtensionField

from Products.CMFPlone.interfaces import IPloneSiteRoot

from abstract.richdescription import MessageFactory as _
from abstract.richdescription.browser.richdescriptionprefs import IRichDescriptionForm
from abstract.richdescription.interfaces import (IAbstractRichDescriptionLayer,
                                            IRichDescriptionExtenderable)


class RichTextField(ExtensionField, atapi.TextField):
    """rich text field extension"""


class RichDescriptionExtender(object):
    adapts(IRichDescriptionExtenderable)
    implements(ISchemaModifier, IOrderableSchemaExtender,
                                            IBrowserLayerAwareExtender)

    layer = IAbstractRichDescriptionLayer

    fields = [
        RichTextField('rich_description',
            required=False,
            searchable=True,
            storage=atapi.AnnotationStorage(migrate=True),
            validators=('isTidyHtmlWithCleanup',),
            default_output_type='text/x-html-safe',
            widget=atapi.RichWidget(
                    description='',
                    label=_(u'Rich description'),
                    rows=25,
                    allow_file_upload=zconf.ATDocument.allow_document_upload),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def apply_extender(self):
        portal = getUtility(IPloneSiteRoot)
        ard_prefs = IRichDescriptionForm(portal)
        if ard_prefs.richdescription_properties is not None:
            portal_type = getattr(self.context, 'portal_type', None)
            if portal_type in ard_prefs.allowed_types:
                return True
        return False

    def fiddle(self, schema):
        """Fiddle the schema.

        This is a copy of the class' schema, with any ISchemaExtender-provided
        fields added. The schema may be modified in-place: there is no
        need to return a value.

        In general, it will be a bad idea to delete or materially change
        fields, since other components may depend on these ones.

        If you change any fields, then you are responsible for making a copy of
        them first and place the copy in the schema.
        """
        # Modify 'description' field visibility
        if schema.get('description'):
            if self.apply_extender():
                field = schema['description'].copy()
                field.widget.visible = {'view': 'invisible',
                                        'edit': 'invisible'}
                schema['description'] = field

        return schema

    def getFields(self):
        if self.apply_extender():
            return self.fields
        return []

    def getOrder(self, original):
        """
        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.
        """
        default = original.get('default', None)
        if default:
            desc_index = 0
            # if there is no title nor description field, do nothing
            if 'description' in default:
                desc_index = default.index('description')
            elif 'title' in default:
                desc_index = default.index('title')
            if desc_index >= 0 and ('rich_description' in default):
                default.remove('rich_description')
                default.insert(desc_index + 1, 'rich_description')
        return original
