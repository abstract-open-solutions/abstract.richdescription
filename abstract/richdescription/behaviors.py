from zope.interface import implementer
from zope.interface import alsoProvides
from zope.component import adapter
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.app.textfield import RichText
from abstract.richdescription import MessageFactory as _


class IRichDescriptionBehavior(model.Schema):

    rich_description = RichText(
        title=_(u"Description"),
        required=False,
        default=u""
    )


@adapter(IDexterityContent)
@implementer(IRichDescriptionBehavior)
class RichDescriptionBehavior(object):

    def __init__(self, context):
        self.context = context

alsoProvides(IRichDescriptionBehavior, IFormFieldProvider)
