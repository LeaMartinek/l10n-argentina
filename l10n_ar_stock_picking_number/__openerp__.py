# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Aconcagua Team (http://www.proyectoaconcagua.com.ar)
#    All Rights Reserved. See AUTHORS for details.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Numeracion Remitos Argentina",
    "version": "1.0",
    "depends": ["base", "stock", "sale_stock"],
    "author": "E-MIPS",
    "website": "http://www.proyectoaconcagua.com.ar",
    "license": "GPL-3",
    "category": "Localization",
    "description": """
    """,
    "data": [
        'wizard/cancel_picking_done_view.xml',
        'stock_view.xml',
        'stock_sequence.xml',
    ],
    'demo': [
        ],
    'test': [
    ],
    'installable': True,
    'active': False,
}
