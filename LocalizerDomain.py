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

"""LocalizerDomain

A translator calling into a Localizer message catalog.
"""

from LocalizerMessageCatalog import LocalizerMessageCatalog

from Domain import Domain

class LocalizerDomain(Domain):

    def __init__(self, path):
        self._path = path

    def getMessageCatalog(self, lang=None):
        return LocalizerMessageCatalog(self._path, lang=lang).__of__(self)



#from DomainHandler import registerDomainHandler

## class LocalizerDomainHandler:

##     def recognizes(self, ob):
##         """Return a domain based on that message catalog."""
##         return ob.meta_type == 'MessageCatalog':

##     def getDomain(self, ob):
##         """Return a domain based on that message catalog."""
##         return LocalizerDomain(ob)


#registerDomainHandler(LocalizerDomainHandler())
