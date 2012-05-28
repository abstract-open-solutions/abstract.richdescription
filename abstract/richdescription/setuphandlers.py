from Products.CMFCore.utils import getToolByName

    
def removeConfiglet(context):
    if context.readDataFile('ard-uninstall.txt') is None:
        return
    site = context.getSite()
    portal_conf = getToolByName(site, 'portal_controlpanel')
    portal_conf.unregisterConfiglet('AbstractRichDescription')
