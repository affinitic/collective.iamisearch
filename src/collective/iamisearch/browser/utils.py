# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from cgi import escape
from collective.iamisearch.interfaces import IIAmFolder
from collective.iamisearch.interfaces import IISearchFolder
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getMultiAdapter
from zope.component import getUtility


class UtilsView(BrowserView):
    """
    """

    def calculate_title(self):
        """
        """
        context_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_context_state"
        )
        page_title = escape(safe_unicode(context_state.object_title()))
        taxonomy_term = self.request.form.get("taxonomy_term")
        if not taxonomy_term:
            return page_title
        current_lang = api.portal.get_current_language()[:2]
        normalizer = getUtility(IIDNormalizer)
        if IIAmFolder.providedBy(self.context):
            taxonomy = getUtility(ITaxonomy, name="collective.taxonomy.iam")
        elif IISearchFolder.providedBy(self.context):
            taxonomy = getUtility(ITaxonomy, name="collective.taxonomy.isearch")
        else:
            return page_title
        data = taxonomy.inverted_data.get(current_lang)
        for key, value in data.items():
            normalized_value = normalizer.normalize(value)
            if normalized_value == taxonomy_term:
                page_title = u"{0} : <span id='taxonomy_term'>{1}</span>".format(
                    page_title, value.lstrip("/")
                )
                break
        return page_title
