from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IRichDescriptionExtenderable(Interface):
    """Rich text field extendarable interface
    """


class IAbstractRichDescriptionLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
