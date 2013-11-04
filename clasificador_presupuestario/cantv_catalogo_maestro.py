# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from osv import fields, osv, orm


class cantv_catalogo_maestro(osv.osv):
    _name = 'cantv.catalogo.maestro'
    
    _columns = {
        'name': fields.char('Nombre', required=True, size=255),
        'descripcion': fields.text('Descripción', help='Descripción', required=True ),        
        'active': fields.boolean('Activo'),
        'detalle': fields.one2many('cantv.catalogo.detalle', 'cantv_catalogo_maestro_id', 'Detalle', required=True,),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
                        ('name_uniq', 'unique (name)','Datos ya existe'),
    ]

    _order = 'name'
    
cantv_catalogo_maestro()


class cantv_catalogo_detalle(osv.osv):
    _name = 'cantv.catalogo.detalle'
    
    _columns = {
                'cantv_catalogo_maestro_id': fields.many2one('cantv.catalogo.maestro', 'Catalogo Maestro Id', 'datos', required=True, ondelete='cascade'),
                'prefijo': fields.char('Prefijo', required=True, size=8 ),
                'name': fields.char('Nombre', required=True, size=255),
                'active': fields.boolean('Activo'),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
                        ('name_uniq', 'unique (codigo,name)','Datos ya existe'),
    ]

    _order = 'name' 
                   
    
cantv_catalogo_detalle()
