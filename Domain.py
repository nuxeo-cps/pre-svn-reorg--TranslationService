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

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from OFS.SimpleItem import SimpleItem


import re

# regexps taken from Zope 3 to interpolate variables
NAME_RE = r"[a-zA-Z][a-zA-Z0-9_]*"
_interp_regex = re.compile(r'(?<!\$)(\$(?:%(n)s|{%(n)s}))' %({'n': NAME_RE}))
_get_var_regex = re.compile(r'%(n)s' %({'n': NAME_RE}))


class Domain(SimpleItem):
    """Translation domain."""

    meta_type = 'Persistent Domain'

    # __implements__ =  IDomain

    def __init__(self, domain):
        self._domain = domain

    def getMessageCatalog(self, lang=None):
        """Get the message catalog implementing this domain."""
        raise 'NotImplemented'

    #
    # IDomain API
    #

    def translate(self, msgid, mapping=None,
                  context=None, target_language=None):
        """Translate a msgid, maybe doing ${keyword} substitution.

        msgid is the message id to be translated.
        mapping is a set of mapping to be applied on ${keywords}.
        """
        # msgid can be '${name} was born in ${country}'.
        # mapping can be {'country': 'Antarctica', 'name': 'Lomax'}.
        # context must be adaptable to IUserPreferredLanguages.

        mc = self.getMessageCatalog(lang=target_language)
        msgid = msgid.strip()
        text = mc.getMessage(msgid)
        return self._interpolate(text, mapping)

    #
    # Internal
    #

    def _interpolate(self, text, mapping):
        """Interpolate ${keyword} substitutions."""
        # Code taken from Zope 3

        if not mapping:
            return text

        # Find all the spots we want to substitute.
        to_replace = _interp_regex.findall(text)

        # Now substitute with the variables in mapping.
        for string in to_replace:
            var = _get_var_regex.findall(string)[0]
            text = text.replace(string, mapping.get(var))

        return text


class DummyDomain(Domain):
    def translate(self, msgid, mapping=None,
                  context=None, target_language=None):
        return '[(%s)%s]' % (self._domain, msgid)
