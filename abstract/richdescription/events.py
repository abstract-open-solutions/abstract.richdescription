# -*- coding: utf-8 -*-
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent
from abstract.richdescription.behaviors import IRichDescriptionBehavior
from browser.richdescriptionprefs import IRichDescriptionForm


def set_plain_description(obj, evt):  # pylint: disable=W0613
    """
    if obj has "rich_description" field, we have to:
    1. strip html tags from rich_description
    2. set description with cleaned text
    """
    portal = getUtility(IPloneSiteRoot)
    ard_prefs = IRichDescriptionForm(portal)
    if ard_prefs.richdescription_properties is not None:
        portal_type = getattr(obj, 'portal_type', None)
        if portal_type in ard_prefs.allowed_types:
            rich_description = ''
            if IDexterityContent.providedBy(obj):
                adapts = IRichDescriptionBehavior(obj, None)
                if adapts:
                    rich_description = adapts.rich_description.output
            else:
                field = obj.getField('rich_description')
                if field:
                    rich_description = field.get(obj)

            plain_text = ''
            if rich_description:
                transforms = getToolByName(portal, 'portal_transforms')
                data = transforms.convert('html_to_text', rich_description)
                plain_text = data.getData()
            plain_text = plain_text.strip()
            plain_text = plain_text.replace('\n', ' ').replace('\r', '')
            obj.setDescription(plain_text)
            obj.reindexObject(idxs=['Description'])
