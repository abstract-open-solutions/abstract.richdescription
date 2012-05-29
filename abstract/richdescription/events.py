# -*- coding: utf-8 -*-
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

from abstract.richdescription.richdescriptionprefs import IRichDescriptionForm


def set_plain_description(obj, evt):
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
            field = obj.getField('rich_description')
            if field:
                rich_description = field.get(obj)
            
            if rich_description:
                transforms = getToolByName(portal, 'portal_transforms')
                data = transforms.convert('html_to_text', rich_description)
                plain_text = data.getData()
                obj.setDescription(plain_text)
                obj.reindexObject()
