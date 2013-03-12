import transaction

from Products.Five.browser import BrowserView


class FixEmpty(BrowserView):
    """ View for fixing those objects that had a rich description
    but no longer have. Running this view is required if you installed
    and used this package previous to version 1.0.1
    """

    def __call__(self):
        portal = self.context

        catalog = portal.portal_catalog
        ard_prefs = portal.portal_properties.richdescription_properties

        portal_type = list(ard_prefs.allowed_types)

        brains = catalog(portal_type=portal_type)
        for i, brain in enumerate(brains):
            print i
            obj = brain.getObject()
            field = obj.getField('rich_description')
            if field:
                rich_description = field.get(obj)
                if not rich_description:
                    # let's clean up description
                    obj.setDescription("")
                    obj.reindexObject(idxs=['Description'])
                    print 'FIXED', brain.getPath()
            else:
                print 'NO FIELD', brain.getPath()
            if i % 500:
                transaction.savepoint(optimistic=1)

        transaction.commit()
        return 'DONE!'
