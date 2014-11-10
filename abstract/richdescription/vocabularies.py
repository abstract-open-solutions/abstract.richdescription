from Acquisition import aq_get
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from zope.i18n import translate
from zope.component import getAllUtilitiesRegisteredFor
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName


class ArcheTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        ptool = getToolByName(site, 'plone_utils', None)
        ttool = getToolByName(site, 'portal_types', None)

        # TODO: check is plone.app.contenttypes is installed
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        dexterity_types = [fti.__name__ for fti in ftis]

        if ptool is None or ttool is None:
            return SimpleVocabulary([])

        request = aq_get(ttool, 'REQUEST', None)
        items = [(translate(ttool[t].Title(), context=request), t)
                 for t in ptool.getUserFriendlyTypes()
                 if not t in dexterity_types]

        items.sort()
        items = [
            SimpleTerm(i[1], i[1], i[0]) for i in items
        ]

        return SimpleVocabulary(items)

ArcheTypesVocabularyFactory = ArcheTypesVocabulary()
