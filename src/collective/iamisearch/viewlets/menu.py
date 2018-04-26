# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MenuViewlet(common.ViewletBase):

    index = ViewPageTemplateFile('menu.pt')

