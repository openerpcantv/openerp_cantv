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

import time
from openerp.osv import fields, osv, orm

#NIVEL DEL CLASFIFICADOR

class cantv_pre_nivel_clasificador(osv.osv):
	_name = "cantv.pre.nivel.clasificador"
	_columns = {
		'cantv_pre_config_clasificador_id': fields.many2one('cantv.pre.config.clasificador', 'Configuracion Clasificador', required=True),
		'cantv_catalogo_detalle_id': fields.many2one('cantv.catalogo.detalle', 'Detalle Catalogo', required=True),
		'nivel':  fields.integer('Nivel', required=True),
		'longitud' : fields.integer('Longitud', required=True),
		'name': fields.char('Nombre', required=True, size=250 ),
		'active': fields.boolean('Activo'),
	}
    
	_defaults = {
		'active': True, 
	}

	_sql_constraints = [
		('def_nivel_uniq', 'unique(cantv_pre_config_clasificador_id, cantv_catalogo_detalle_id, nivel, name)',
		'La configuracion del nivel que desea crear ya existe'),
	]

	def write(self,cr, uid, ids, vals, context=None):

		# Verifica que el nivel no sea mayor al definido en la configuracion del clasificador
		cr.execute('SELECT cantv_pre_config_clasificador_id FROM cantv_pre_nivel_clasificador where id=%s',(ids[0],))
		res = cr.fetchone()
		if res:
			obj = self.pool.get('cantv.pre.config.clasificador').search(cr, uid, [('id','=',res[0])])
			result = self.pool.get('cantv.pre.config.clasificador').browse(cr, uid, obj)
			if "nivel" in vals:
				if vals["nivel"] > result[0]['nivel']:
					raise orm.except_orm('Nivel invalido',"El nivel no puede ser mayor a %s"%(result[0]['nivel']))
					return False

		# Verifica que la longitud de un nivel despues de editar, sea igual a los credaos anteriormente
		if 'longitud' in vals and 'nivel' in vals:
			cr.execute('SELECT longitud, nivel from cantv_pre_nivel_clasificador where cantv_pre_config_clasificador_id=( '+
					'select cantv_pre_config_clasificador_id from cantv_pre_nivel_clasificador where id=%s) and nivel=%s',(ids[0],vals["nivel"],))
			res = cr.fetchone()
			if res:
				if res[0] != vals["longitud"] and res[1] == vals["nivel"]:
					raise orm.except_orm('Longitud invalida',"La longitud debe ser igual a %s"%(res[0]))
					return False
		elif 'longitud' in vals:
			obj = self.pool.get('cantv.pre.nivel.clasificador').search(cr, uid, [('id','=',ids[0])])
			result = self.pool.get('cantv.pre.nivel.clasificador').browse(cr, uid, obj)

			if vals["longitud"] != result[0]['longitud']:
				raise orm.except_orm('Longitud invalida',"La longitud debe ser igual a %s"%(result[0]['longitud']))
				return False

		elif 'nivel' in vals:
			cr.execute('SELECT longitud, nivel from cantv_pre_nivel_clasificador where cantv_pre_config_clasificador_id=( '+
					'select cantv_pre_config_clasificador_id from cantv_pre_nivel_clasificador where id=%s) and nivel=%s',(ids[0],vals["nivel"],))
			res = cr.fetchone()
			if res:
				obj = self.pool.get('cantv.pre.nivel.clasificador').search(cr, uid, [('id','=',ids[0])])
				result = self.pool.get('cantv.pre.nivel.clasificador').browse(cr, uid, obj)

				if res[0] != result[0]['longitud'] and res[1] == vals["nivel"]:
					raise orm.except_orm('Longitud invalida',"La longitud debe ser igual a %s"%(res[0]))
					return False
		
		return super(cantv_pre_nivel_clasificador, self).write(cr, uid, ids, vals, context=context)
	
	def create(self, cr, uid, vals, context=None):

		# Verifica que el nivel no sea mayor al definido en la configuracion del clasificador
		obj = self.pool.get('cantv.pre.config.clasificador').search(cr, uid, [('id','=',vals["cantv_pre_config_clasificador_id"])])
		result = self.pool.get('cantv.pre.config.clasificador').browse(cr, uid, obj)

		if vals["nivel"] > result[0]['nivel']:
			raise orm.except_orm('Nivel invalido',"El nivel no puede ser mayor a %s"%(result[0]['nivel']))
			return False

		# Verifica que la longitud del nivel a crear sea igual a los creados anteriormente
		obj = self.pool.get('cantv.pre.nivel.clasificador').search(cr, uid, ['&',('cantv_pre_config_clasificador_id','=',vals["cantv_pre_config_clasificador_id"]),('nivel','=',vals["nivel"])])
		result = self.pool.get('cantv.pre.nivel.clasificador').browse(cr, uid, obj)

		if result:
			if vals["longitud"] != result[0]['longitud']:
				raise orm.except_orm('Longitud invalida',"La longitud debe ser igual a %s"%(result[0]['longitud']))
				return False

		return super(cantv_pre_nivel_clasificador, self).create(cr, uid, vals, context=context)

cantv_pre_nivel_clasificador()
