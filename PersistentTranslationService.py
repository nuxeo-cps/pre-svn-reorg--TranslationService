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

"""PersistentTranslationService

Provides a persistent configurable translation service that can call
into different message catalogs.
"""

from zLOG import LOG, DEBUG
from Globals import InitializeClass
from Globals import DTMLFile
from AccessControl import ClassSecurityInfo

from OFS.SimpleItem import SimpleItem


from Domain import DummyDomain
from LocalizerDomain import LocalizerDomain


# Permission
ManageTranslationServices = 'Manage Translation Services'


# Constructors
addPersistentTranslationServiceForm = DTMLFile(
    'zmi/addPersistentTranslationServiceForm', globals())

def addPersistentTranslationService(dispatcher, id, REQUEST=None):
    """Adds a PersistentTranslationService."""
    ob = PersistentTranslationService(id)
    container = dispatcher.Destination()
    container._setObject(id, ob)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)


class PersistentTranslationService(SimpleItem):
    """ZODB-based Translation Service."""

    meta_type = 'Persistent Translation Service'

    security = ClassSecurityInfo()
    security.declareObjectPrivate()

    _domain_dict = {None: ''}
    _domain_list = (None,) # for UI ordering

    def __init__(self, id):
        self.id = id

    #
    # Internal
    #

    security.declarePublic('test')
    def test(self, msgid='nomsgid'):
        """Test."""
        return self.translate('default', msgid)

    # __implements__ =  ITranslationService

    #
    # Internal API
    #

    def _getDomain(self, domain):
        """Get the domain."""
        path = self._domain_dict.get(domain)
        if path is None:
            return None

        if path.endswith('.mo'):
            # filesystem .mo
            return None

        try:
            ob = self.unrestrictedTraverse(path)
        except:
            ob = None

        if ob is not None:
            # Points to an object
            if ob.meta_type == 'MessageCatalog':
                # Localizer
                return LocalizerDomain(path).__of__(self)
            else:
                return None

        else:
            # not an object
            return None

    #
    # ITranslationService API
    #

    def getDomain(self, domain):
        """Get the domain for the passed domain name."""

        # We have to lookup a message catalog in the ZODB but
        # cache some stuff otherwise things are going to be slow.
        request = self.REQUEST.other
        cache = request.get('_ts_domain_cache')
        if cache is None:
            cache = {}
            request['_ts_domain_cache'] = cache
        if cache.has_key(domain):
            return cache[domain]

        dom = self._getDomain(domain)
        if dom is None:
            # Use default if available
            dom = cache.get(None)
            if dom is None:
                dom = self._getDomain(None)
        if dom is None:
            dom = DummyDomain(domain)

        cache[domain] = dom

        return dom


    def translate(self, domain, *args, **kw):
        return self.getDomain(domain).translate(*args, **kw)

    #
    # ZMI
    #

    manage_options = ({'label': 'Configuration',
                       'action': 'manage_configure',
                       },
                      ) + SimpleItem.manage_options

    security.declareProtected(ManageTranslationServices, 'manage_configure')
    manage_configure = DTMLFile('zmi/manage_configure', globals())

    #
    # ZMI Configuration
    #

    security.declareProtected(ManageTranslationServices, 'getDomainInfo')
    def getDomainInfo(self):
        """Get info on all the recognized domain.

        The None domain represents the default domain."""
        res = []
        for domain in self._domain_list:
            res.append((domain, self._domain_dict[domain]))
        return res


    security.declareProtected(ManageTranslationServices, 'manage_setDomainInfo')
    def manage_setDomainInfo(self, REQUEST=None, **kw):
        """Set domain info."""
        if REQUEST is not None:
            kw.update(REQUEST.form)
        domain_list = list(self._domain_list)
        domain_dict = self._domain_dict.copy()
        for index in range(len(domain_list)):
            domainname = 'domain_%d' % index
            pathname = 'path_%d' % index
            domain = domain_list[index]
            if domain is not None:
                newdomain = kw[domainname]
                if domain != newdomain:
                    domain_list[index] = newdomain
                    domain_dict[newdomain] = domain_dict[domain]
                    del domain_dict[domain]
                domain = newdomain
            path = kw[pathname]
            domain_dict[domain] = path
        # Trigger persistence.
        self._domain_list = tuple(domain_list)
        self._domain_dict = domain_dict
        if REQUEST is not None:
            return self.manage_configure(self, REQUEST,
                                         manage_tabs_message="Changed.")


    security.declareProtected(ManageTranslationServices, 'manage_addDomainInfo')
    def manage_addDomainInfo(self, domain, path,
                             REQUEST=None, **kw):
        """Add domain info."""
        if REQUEST is not None:
            kw.update(REQUEST.form)
        domain_list = list(self._domain_list)
        domain_dict = self._domain_dict.copy()
        if domain_dict.has_key(domain):
            raise KeyError, "Domain %s already exists." % domain
        domain_list.append(domain)
        domain_dict[domain] = path
        # Trigger persistence.
        self._domain_list = tuple(domain_list)
        self._domain_dict = domain_dict
        if REQUEST is not None:
            return self.manage_configure(self, REQUEST,
                                         manage_tabs_message="Added.")

    security.declareProtected(ManageTranslationServices, 'manage_delDomainInfo')
    def manage_delDomainInfo(self, REQUEST=None, **kw):
        """Delete domain info."""
        if REQUEST is not None:
            kw.update(REQUEST.form)
        domain_list = list(self._domain_list)
        domain_dict = self._domain_dict.copy()
        todel = []
        for index in range(len(domain_list)):
            checkname = 'check_%d' % index
            if kw.get(checkname):
                domain = domain_list[index]
                if domain is not None:
                    todel.append(domain)
        for domain in todel:
            domain_list.remove(domain)
            del domain_dict[domain]
        # Trigger persistence.
        self._domain_list = tuple(domain_list)
        self._domain_dict = domain_dict
        if REQUEST is not None:
            return self.manage_configure(self, REQUEST,
                                         manage_tabs_message="Deleted.")


InitializeClass(PersistentTranslationService)
