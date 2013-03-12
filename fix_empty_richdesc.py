# -*- coding: utf-8 -*-
""" a script for cleaning up emtpy rich descriptions
"""

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Testing.makerequest import makerequest
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser

from abstract.richdescription.browser.richdescriptionprefs import IRichDescriptionForm


def spoofRequest(app):
    """
    Make REQUEST variable to be available on the Zope application server.

    This allows acquisition to work properly
    """
    _policy=PermissiveSecurityPolicy()
    _oldpolicy=setSecurityPolicy(_policy)
    newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
    return makerequest(app)

# Enable Faux HTTP request object
app = spoofRequest(app)

portal = app.Plone
catalog = portal.portal_catalog

ard_prefs = IRichDescriptionForm(portal)
portal_type = list(ard_prefs.allowed_types)

brains = catalog(portal_type=portal_type)
for brain in brains:
    obj = brain.getObject()
    field = obj.getField('rich_description')
    if field:
        rich_description = field.get(obj)
        if not rich_description:
            # let's clean up description
            obj.setDescription("")
            obj.reindexObject(idxs=['Description'])

import transaction
transaction.commit()
