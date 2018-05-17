# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.layout.viewlets import common


class MenuViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('menu.pt')

    def generate_menu_value_by_taxonomy_level(self, taxonomy_name, target_level=1, all_path=False):
        """
        :param target_level:
        :return:
        """
        utility = self.get_taxonomy('collective.taxonomy.'+taxonomy_name)
        if not utility.data:
            return None
        target_language = str(utility.getCurrentLanguage(self.request))
        taxonomy_keys = utility.inverted_data[target_language]
        targets_by_level = []
        for key, value in taxonomy_keys.iteritems():
            item = taxonomy_keys[key]
            targets = item[1:].split(PATH_SEPARATOR)
            if all_path:
                if len(targets) == target_level:
                    targets_by_level.append(targets)
            else:
                if len(targets) == target_level:
                    targets_by_level.append(targets[-1])

        return targets_by_level


    def isearchlink(self):
        print"bar"

    def get_taxonomy(self, name):
        portal = api.portal.get()
        sm = portal.getSiteManager()
        sm.queryUtility(ITaxonomy)
        return sm.queryUtility(ITaxonomy, name=name)
