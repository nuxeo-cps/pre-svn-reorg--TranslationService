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

from PersistentTranslationService import PersistentTranslationService
from PersistentTranslationService import addPersistentTranslationServiceForm
from PersistentTranslationService import addPersistentTranslationService
from PersistentTranslationService import ManageTranslationServices

from PersistentTranslationService import PersistentTranslationServiceLookup
from Products.PageTemplates.GlobalTranslationService import \
     setGlobalTranslationService

setGlobalTranslationService(PersistentTranslationServiceLookup())

def initialize(registrar):
    registrar.registerClass(
        PersistentTranslationService,
        permission=ManageTranslationServices,
        constructors=(addPersistentTranslationServiceForm,
                      addPersistentTranslationService),
        icon='translation_service_icon.gif',
        )
