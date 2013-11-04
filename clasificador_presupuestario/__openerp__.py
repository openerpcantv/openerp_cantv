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


{
    'name': 'Configuracion Presupuesto',
    'version': '2.0',
    'category': 'Generic Modules/Configuracion',
    'sequence': 1,
    'summary': 'Clasificador Presupuestario',
    'description': 'Manejo de las cuentas de presupuesto.',
    'author': 'CANTV',
    'website': 'http://www.cantv.com.ve',
    'depends': ['base'],
    'init_xml':[ 
                     'demo/cantv_catalogo_maestro_demo.xml',     
#                    'initial_data/data.xml', 
#                    'initial_data/ppto_plan_operativo_tipo_demo.xml'
                  ],    
    'update_xml': [
                   'views/cantv_pre_config_clasificador_view.xml',
                   'views/cantv_catalogo_maestro_view.xml',
                   'views/cantv_pre_clasificador_presupuestario_view.xml',
                   'views/cantv_pre_nivel_clasificador_view.xml',
                   'cantv_pre_menu.xml'
    ],
    'demo': [
             'demo/cantv_catalogo_maestro_demo.xml',    
#            'demo/ppto_cuenta_presupuestaria_demo.xml',
#            'demo/ppto_fuente_financiamiento_demo.xml',
#            'demo/ppto_unidad_tipo_demo.xml',
#            'demo/ppto_ambito_demo.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
