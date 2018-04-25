# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.iamisearch:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    data_iam = {
        'taxonomy': 'iam',
        'field_title': 'Iam',
        'field_description': 'Iamsearching',
        'default_language': 'fr',
    }

    data_isearch = {
        'taxonomy': 'isearch',
        'field_title': 'Isearch',
        'field_description': 'Iamsearching',
        'default_language': 'fr',
    }
    create_taxonomy_object(data_iam)
    create_taxonomy_object(data_isearch)

    sm = api.portal.get().getSiteManager()
    item = 'collective.taxonomy.test'
    utility = sm.queryUtility(ITaxonomy, name=item)
    utility.unregisterBehavior()
    sm.unregisterUtility(utility, ITaxonomy, name=item)
    sm.unregisterUtility(utility, IVocabularyFactory, name=item)
    sm.unregisterUtility(utility, ITranslationDomain, name=item)


def create_taxonomy_object(data):
    taxonomy = registerTaxonomy(
        api.portal.get(),
        name=data['taxonomy'],
        title=data['field_title'],
        description=data['field_description'],
        default_language=data['default_language']
    )

    del data['taxonomy']
    taxonomy.registerBehavior(**data)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
