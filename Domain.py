# (C) Copyright 2002, 2003 Nuxeo SARL <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
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

import re

from DocumentTemplate.DT_Util import ustr
from OFS.SimpleItem import SimpleItem

try:
    from Globals import get_request
except ImportError:
    get_request = lambda: None

from TAL.TALInterpreter import _interp_regex, _get_var_regex

_charset_regex = re.compile(
    r'text/[0-9a-z]+\s*;\s*charset=([-_0-9a-z]+)(?:(?:\s*;)|\Z)',
    re.IGNORECASE)


def _findEncoding():
    encoding = 'latin1'
    request = get_request()
    if request is not None:
        ct = request.RESPONSE.headers.get('content-type')
        if ct:
            match = _charset_regex.match(ct)
            if match:
                encoding = match.group(1)
    return encoding


class Domain(SimpleItem):
    """Translation domain."""
    # Inherit from a Persistent base class to be able to lookup placefully.

    meta_type = 'Placeful Domain' # XXX unused

    # __implements__ =  IDomain

    def __init__(self, domain):
        self._domain = domain

    def getMessageCatalog(self, lang=None):
        """Get the message catalog implementing this domain."""
        raise NotImplementedError

    #
    # IDomain API
    #

    def translate(self, msgid, mapping=None, context=None, 
                  target_language=None, default=None):
        """Translate a msgid, maybe doing ${keyword} substitution.

        msgid is the message id to be translated.
        mapping is a set of mapping to be applied on ${keywords}.
        """
        # msgid can be '${name} was born in ${country}'.
        # mapping can be {'country': 'Antarctica', 'name': 'Lomax'}.
        # context must be adaptable to IUserPreferredLanguages.

        mc = self.getMessageCatalog(lang=target_language)
        text = mc.queryMessage(msgid, default=default)
        if text is None:
            # No default was passed, and msgid has no translation.
            text = msgid
        return self._interpolate(text, mapping)

    #
    # Internal
    #

    def _interpolate(self, text, mapping):
        """Interpolate ${keyword} substitutions."""
        if not mapping:
            return text

        # Find all the spots we want to substitute.
        to_replace = _interp_regex.findall(text)

        # Now substitute with the variables in mapping.
        encoding = None
        for string in to_replace:
            var = _get_var_regex.findall(string)[0]
            if mapping.has_key(var):
                subst = ustr(mapping[var])
                try:
                    text = text.replace(string, subst)
                except UnicodeError:
                    # The string subst contains high-bit chars.
                    # Assume it's encoded in the output encoding.
                    # (This will be the case if Localizer was used.)
                    if encoding is None:
                        encoding = _findEncoding()
                    subst = unicode(subst, encoding, 'ignore')
                    text = text.replace(string, subst)

        return text


class DummyDomain(Domain):
    def translate(self, *args, **kw):
        return None

