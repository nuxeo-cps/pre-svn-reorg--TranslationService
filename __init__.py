# (C) Copyright 2002 Nuxeo SARL <http://nuxeo.com>
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

from PlacefulTranslationService import PlacefulTranslationService
from PlacefulTranslationService import addPlacefulTranslationServiceForm
from PlacefulTranslationService import addPlacefulTranslationService
from PlacefulTranslationService import ManageTranslationServices

from PlacefulTranslationService import PlacefulTranslationServiceLookup
from Products.PageTemplates.GlobalTranslationService import \
     setGlobalTranslationService

setGlobalTranslationService(PlacefulTranslationServiceLookup())

def initialize(registrar):
    registrar.registerClass(
        PlacefulTranslationService,
        permission=ManageTranslationServices,
        constructors=(addPlacefulTranslationServiceForm,
                      addPlacefulTranslationService),
        icon='translation_service_icon.gif')
