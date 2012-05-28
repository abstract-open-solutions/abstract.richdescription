from zope.interface import Interface
from zope import schema
from plone.theme.interfaces import IDefaultPloneLayer

from abstract.richdescription import MessageFactory as _


class IRichDescriptionSettings(Interface):
    """IRichDescriptionSettings base settings for collective.geo
       describe default property used to display the map
       widgets in Plone
    """
    allowed_types = schema.List(
        title=_(u'Content types with rich description'),
        required=False,
        default=[],  # 'Document', 'News', 'Event', 'Folder'],
        description=_(u"A list of types"),
        value_type=schema.Choice(title=_(u"Content types with rich description"),
                source="plone.app.vocabularies.ReallyUserFriendlyTypes"))


class IRichDescriptionExtenderable(Interface):
    """Rich text field extendarable interface
    """


class IAbstractRichDescriptionLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
