from Acquisition import aq_get
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from zope.i18n import translate
from plone.app.vocabularies.types import BAD_TYPES
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName

import pkg_resources
try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True


class ArcheTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary([])
        items = []
        request = aq_get(ttool, 'REQUEST', None)
        for k, v in ttool.items():
            if HAS_DEXTERITY:
                if IDexterityFTI.providedBy(v):
                    continue

        if k not in BAD_TYPES:
            items.append(
                (k, translate(v.Title(), context=request))
            )

        items.sort(key=lambda x: x[1])
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)

ArcheTypesVocabularyFactory = ArcheTypesVocabulary()
