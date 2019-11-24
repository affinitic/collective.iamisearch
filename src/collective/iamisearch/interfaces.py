# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveIamisearchLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIAmFolder(Interface):
    """Marker interface for I Am folder(s)."""


class IISearchFolder(Interface):
    """Marker interface for I Search folder(s)."""
