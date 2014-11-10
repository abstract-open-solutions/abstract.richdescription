# -*- coding: utf-8 -*-
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from plone.dexterity.interfaces import IDexterityContent
from abstract.richdescription.behaviors import IRichDescriptionBehavior
from richdescriptionprefs import IRichDescriptionForm


class RichDescriptionViewlet(ViewletBase):

    index = ViewPageTemplateFile("templates/rich_description.pt")

    def is_available(self):
        portal = getUtility(IPloneSiteRoot)
        ard_prefs = IRichDescriptionForm(portal)
        if ard_prefs.richdescription_properties is not None:
            portal_type = getattr(self.context, 'portal_type', None)
            if portal_type in ard_prefs.allowed_types:
                return True
        return False

    def getRich_description(self):
        rich_description = ''
        field = None

        if IDexterityContent.providedBy(self.context):
            adapts = IRichDescriptionBehavior(self.context, None)
            if adapts:
                rich_description = adapts.rich_description.output
        else:
            field = self.context.getField('rich_description')
            if field:
                rich_description = field.get(self.context)

        return rich_description
