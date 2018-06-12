# -*- coding: utf-8 -*-
import os

from collective.iamisearch import _

from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from plone.app.multilingual import api as api_lng
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.i18n import translate
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
    # creation of taxonomies
    taxonomies_collection = [_('I am'), _('I search')]
    data_iam = {
        'taxonomy': 'iam',
        'field_title': _('I am'),
        'field_description': _('I am searching'),
        'default_language': 'fr',
    }

    data_isearch = {
        'taxonomy': 'isearch',
        'field_title': _('I search'),
        'field_description': _('I search'),
        'default_language': 'fr',
    }

    faced_config = {
        'I am': '/faceted/config/iam_folder.xml',
        'I search': '/faceted/config/isearch_folder.xml',
    }

    # install taxonomy
    portal = api.portal.get()
    sm = portal.getSiteManager()
    iam_item = 'collective.taxonomy.iam'
    isearch_item = 'collective.taxonomy.isearch'
    utility_iam = sm.queryUtility(ITaxonomy, name=iam_item)
    utility_isearch = sm.queryUtility(ITaxonomy, name=isearch_item)

    # stop installation if already
    # if utility_iam and utility_isearch:
    #     return
    create_taxonomy_object(data_iam)
    create_taxonomy_object(data_isearch)
    #  remove taxonomy test
    item = 'collective.taxonomy.test'
    utility = sm.queryUtility(ITaxonomy, name=item)
    if utility:
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=item)
        sm.unregisterUtility(utility, IVocabularyFactory, name=item)
        sm.unregisterUtility(utility, ITranslationDomain, name=item)

    # creation of two collections by language
    language_tool = api.portal.get_tool('portal_languages')
    langs = language_tool.supported_langs
    current_lang = api.portal.get_current_language()[:2]
    container = api.portal.get().get(current_lang)
    if container is None:
        container = api.portal.get()
    for taxonomy_collection in taxonomies_collection:
        title = taxonomy_collection
        normalizer = getUtility(IIDNormalizer)
        if normalizer.normalize(title) not in container:
            new_obj = api.content.create(
                type='Folder',
                title=translate(_(title), target_language=current_lang),
                container=container)
            try:
                nav = IExcludeFromNavigation(new_obj)
            except:
                pass
            if nav:
                nav.exclude_from_nav = True
            new_obj.reindexObject()
            _activate_dashboard_navigation(new_obj, faced_config[taxonomy_collection])
            for lang in langs:
                if lang != current_lang:
                    translated_obj = translation_folderish(new_obj, lang)
                    _activate_dashboard_navigation(translated_obj, faced_config[taxonomy_collection])


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


def translation_folderish(obj, lang):
    translated_obj = api_lng.translate(obj, lang)
    translated_obj.title = translate(_(obj.title), target_language=lang)
    try:
        nav = IExcludeFromNavigation(translated_obj)
    except:
        pass
    if nav:
        nav.exclude_from_nav = True
    translated_obj.reindexObject()
    return translated_obj


def _activate_dashboard_navigation(context, config_path=''):
    subtyper = context.restrictedTraverse('@@faceted_subtyper')
    if subtyper.is_faceted:
        return
    subtyper.enable()
    context.unrestrictedTraverse('@@faceted_exportimport').import_xml(
        import_file=open(os.path.dirname(__file__) + config_path)
    )


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
