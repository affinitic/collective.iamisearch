# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from collective.iamisearch import _
from Products.CMFPlone.interfaces import ILanguage
from zope.i18n import translate


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.iamisearch:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # creation of taxonomies
    taxonomies_collection = ['Iam', 'Isearch']
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
    #  remove taxonomy test
    portal = api.portal.get()
    sm = portal.getSiteManager()
    item = 'collective.taxonomy.test'
    utility = sm.queryUtility(ITaxonomy, name=item)
    utility.unregisterBehavior()
    sm.unregisterUtility(utility, ITaxonomy, name=item)
    sm.unregisterUtility(utility, IVocabularyFactory, name=item)
    sm.unregisterUtility(utility, ITranslationDomain, name=item)

    # creation of two collections by language
    language_tool = api.portal.get_tool('portal_languages')
    langs = language_tool.supported_langs
    for taxonomy_collection in taxonomies_collection:
        title = "{0}_collection".format(taxonomy_collection)
        create_folderish('Collection', title, api.portal.get(), langs)


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


def create_folderish(type_content, title, parent, langs):
    new_obj = api.content.create(
        type=type_content,
        title=title,
        container=parent)
    language = ILanguage(new_obj).get_language()
    for lang in langs:
        if language == lang:
            continue
        else:
            new_obj.title = translate(_(title), target_language=lang)

    new_obj.reindexObject()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
