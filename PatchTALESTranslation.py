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

def _dummy_translate(domain, msgid, *args, **kw):
    return '[(%s)%s]' % (domain, msgid)


from Products.PageTemplates.TALES import Context

def translate(self, *args, **kw):
    # Are we called in a placeful way?
    contexts = self.contexts
    here = contexts.get('here')
    if here is None:
        # Placeless!
        return _dummy_translate(*args, **kw)
    # Find a placeful translation service
    request = contexts.get('request')
    assert request != None, 'request should not be None'
    request = request.other
    translation_service = request.get('_translation_service_cache')
    if translation_service is None:
        # Find it by acquisition
        translation_service = getattr(here, 'translation_service', None)
        if translation_service is None:
            return _dummy_translate(*args, **kw)
        request['_translation_service_cache'] = translation_service
    return translation_service.translate(*args, **kw)

Context.translate = translate
