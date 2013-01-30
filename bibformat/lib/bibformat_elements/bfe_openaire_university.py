# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.openaire_deposit_config import CFG_OPENAIRE_THESIS_TYPES


def format_element(bfo):
    ln = bfo.lang

    info = bfo.field('502__')

    if not info:
        return ""

    ret = ""
    if 'b' in info and 'c' in info:
        ret = "%(type)s, %(university)s"
    elif 'b' in info:
        ret = "%(type)s"
    elif 'c' in info:
        ret = "%(university)s"

    try:
        type_title = dict(CFG_OPENAIRE_THESIS_TYPES(ln))[info['b']]
    except KeyError:
        type_title = ''

    ctx = {
        'university': info['c'],
        'type': type_title,
    }

    return ret % ctx


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
