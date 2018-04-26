# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.layout.viewlets import common


class MenuViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('menu.pt')

    def iamlink(self):
        utility = self.get_taxonomy('collective.taxonomy.iam')
        # WIP
        keys = utility.data['fr'].keys()

    def isearchlink(self):
        print"bar"

    def get_taxonomy(self, name):
        portal = api.portal.get()
        sm = portal.getSiteManager()
        sm.queryUtility(ITaxonomy)
        return sm.queryUtility(ITaxonomy, name=name)
