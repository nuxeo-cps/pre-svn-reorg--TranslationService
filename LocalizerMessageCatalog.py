# Copyright (C) 2002 Nuxeo SARL <http://nuxeo.com>
# Copyright (C) 2002 Florent Guillaume <mailto:fg@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

"""LocalizerMessageCatalog

A Localizer Message Catalog
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from OFS.SimpleItem import SimpleItem


class LocalizerMessageCatalog(SimpleItem):

    meta_type = 'Persistent Localizer Message Catalog'

    security = ClassSecurityInfo()
    security.declareObjectPrivate()

    def __init__(self, path, lang=None):
        self._path = path
        self._lang = lang

    def _getLocalizerMessageCatalog(self, path):
        try:
            mc = self.unrestrictedTraverse(path)
        except:
            mc = None
        return mc

    def getMessage(self, id):
        """Get a message from the message catalog."""
        # Find in the request cache if we have already traversed to
        # the message catalog.
        request = self.REQUEST.other
        cache = request.get('_localizer_persistent_mc_cache')
        if cache is None:
            cache = {}
            request['_localizer_persistent_mc_cache'] = cache
        path = self._path
        if cache.has_key(path):
            mc = cache[domain]
        else:
            mc = self._getLocalizerMessageCatalog(path)

        if mc is None:
            mc = DummyMessageCatalog() # XXX

        id = id.strip()
        text = mc.gettext(id, lang=self._lang)
        return text

    def queryMessage(self, id, default=None):
        """Get a message from the message catalog."""
        # Localizer's Message Catalog has no way to default.
        return self.getMessage(id)





#from DomainHandler import registerDomainHandler

## class LocalizerDomainHandler:

##     def recognizes(self, ob):
##         """Return a domain based on that message catalog."""
##         return ob.meta_type == 'MessageCatalog':

##     def getDomain(self, ob):
##         """Return a domain based on that message catalog."""
##         return LocalizerDomain(ob)


#registerDomainHandler(LocalizerDomainHandler())
