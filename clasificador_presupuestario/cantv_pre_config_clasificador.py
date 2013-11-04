# -*- coding: utf-8 -*-
###############################################################################
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

import datetime
from openerp.osv import fields, osv

#CONFIGURACION DEL CLASFIFICADOR

class cantv_pre_config_clasificador(osv.osv):
    _name = "cantv.pre.config.clasificador"
    _columns = {
        'name': fields.char('Nombre', required=True, size=150),
        'desde': fields.date('Fecha Inicio', required=True, help='Fecha de vigencia desde.'),
        'hasta': fields.date('Fecha Fin', required=True, help='Fecha de vigencia hasta.'),
        'nivel' : fields.integer('Nivel', size=2, required=True),
        'active': fields.boolean('Activo'),
    }
    
    _defaults = {
        'active': True,
        'desde': datetime.date.today().strftime('%Y-01-01'),
        'hasta': datetime.date.today().strftime('%Y-12-31'),
    }
    
    _sql_constraints = [
                        ('name_uniq', 'unique (name)','El nombre ya existe'),
    ]
cantv_pre_config_clasificador()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
