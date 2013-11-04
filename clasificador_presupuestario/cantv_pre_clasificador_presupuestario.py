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

import re
from openerp.osv import fields, osv,orm
from types import *

#libreria propia de open erp
import datetime
from openerp.osv import fields, osv

class cantv_pre_clasificador_presupuestario(osv.osv):
    """ Clasificador Presupuestario """
    _name = 'cantv.pre.clasificador.presupuestario'
    
    _columns = {
        'parent_id': fields.many2one('cantv.pre.clasificador.presupuestario', 'Clasificador presupuestario (padre)', ondelete='cascade', onupdate='cascade',),
        'historico_id': fields.many2one('cantv.pre.clasificador.presupuestario', 'Histórico'),
        'cantv_pre_nivel_clasificador_id': fields.many2one('cantv.pre.nivel.clasificador','Nivel'),
        'cantv_catalogo_detalle_id': fields.many2one('cantv.catalogo.detalle','Tipo'),
        'cantv_pre_config_clasificador_id': fields.many2one('cantv.pre.config.clasificador','Clasificador',required=True),
        'child_ids':fields.one2many('cantv.pre.clasificador.presupuestario', 'parent_id', 'Hijos'),
        'name': fields.char('Denominación', required=True, help='Nombre del plan operativo (PO)'),
        'codigo': fields.char('Código', required=True, help='Código del plan operativo'),
        'descripcion': fields.text('Descripción', required=True, help='Descripción del plan operativo'),
        'observacion': fields.text('Observación', help='Observación del plan operativo'),
        'desde': fields.date('Fecha Inicio', required=True, help='Fecha desde la que empieza a aplicar el PO'),
        'hasta': fields.date('Fecha Fin', required=True, help='Fecha en la que vence el PO.'),
        'active': fields.boolean('Activo', required=True),
    }

    #valores por defecto para los campos
    _defaults = {                 
        'active':True,
        'desde':datetime.date.today().strftime('%Y-01-01'),
        'hasta':datetime.date.today().strftime('%Y-12-31')}

    #define el orden de los registros en la tabla de consulta
    _order = 'codigo'

    _sql_constraints = [('name_uniq', 'unique (name)', 'Denominación del plan operativo, ya existe')]

    #Verifica que se tenga un rango de fechas valido
    def verifica_fecha(self, cr, uid, ids, desde, hasta, active, context=None):
            retorno={}
            if desde and hasta:#se deben recibir 2 fechas para comparar
                if datetime.datetime.strptime(desde,'%Y-%m-%d') > datetime.datetime.strptime(hasta,'%Y-%m-%d'):
                        retorno["desde"]=desde
                        retorno["hasta"]=desde
                        alerta = {'title':'Rango de fechas inválido', 'message':'La fecha fin no debe ser menor que la fecha de inicio'}
                        return {'warning': alerta, 'value': retorno}
                else:
                        return True
            else:
                    return False
                
    #reescribe el metodo por defecto para mostrar un nombre descriptivo en los selects
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        
        param_list=[]
        
        sql="SELECT id, codigo FROM cantv_pre_clasificador_presupuestario"

        cr.execute(sql,param_list)
        #extra los resultados en un diccionario
        res=cr.dictfetchall()
        res = [(r['id'], r['codigo']) for r in res]
        return res     
    
    #reescribe el metodo por defecto para mostrar un nombre descriptivo para un registro
    def name_get(self, cr, user, ids, context=None):

        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        
        #se extraen los elementos de la lista separados por ,        
        elementos=",".join([str(i) for i in ids])
        sql="SELECT id, codigo FROM cantv_pre_clasificador_presupuestario where id in ("+elementos+")"
        cr.execute(sql)
        res=cr.dictfetchall()
        res = [(r['id'], r['codigo']) for r in res]
        return res
                
                                
    #Campo observación es obligatorio cuando ocurre una modificación
    def write(self, cr, uid, ids, vals, context=None):
            if not 'observacion' in vals:
                    raise orm.except_orm('Campo obligatorio',"El campo observacion es obligatorio")
                    return False
            elif vals['observacion']=='':
                    raise orm.except_orm('Campo obligatorio',"El campo observacion es obligatorio")
                    return False
            return super( cantv_pre_clasificador_presupuestario, self).write(cr, uid, ids, vals, context=context)
    
    
    def checkcodigo(self, cr, uid, ids, codigo, cantv_pre_config_clasificador_id):
            #Valida que el campo codigo solo permita números
            if codigo != False:
                if re.match("^[0-9]+$", codigo) == None:
                    alerta = {'title':'Error !', 'message':' En  este  campo  solo  se  permiten  numeros . . .'}
                    return {'warning': alerta}
            #Valida que la longitud del campo codigo no sea menor o mayor a la longitud definida en el nivel del clasificador
            if codigo:
                cr.execute('select sum(b.longitud) as longitud from cantv_pre_config_clasificador a '
                           +'inner join cantv_pre_nivel_clasificador b on a.id=b.cantv_pre_config_clasificador_id '+
                           'where a.id=%s and b.cantv_catalogo_detalle_id=(select distinct b.cantv_catalogo_detalle_id  from cantv_pre_config_clasificador a '+
                           'inner join cantv_pre_nivel_clasificador b on a.id=b.cantv_pre_config_clasificador_id '+
                           'where a.id=%s limit 1)',(cantv_pre_config_clasificador_id,cantv_pre_config_clasificador_id,))
                longitud_mascara= cr.fetchone()
                if len(codigo)>longitud_mascara:
                    raise orm.except_orm('Codigo Invalido',"El codigo no puede ser mayor a: %s"%(longitud_mascara[0],))
                    return False
                elif len(codigo)<longitud_mascara:
                    raise orm.except_orm('Codigo Invalido',"El codigo no puede ser menor a: %s"%(longitud_mascara[0],))
                    return False
                
                cr.execute('select sum(longitud) as longitud_padre from cantv_pre_nivel_clasificador '+
                           'where cantv_catalogo_detalle_id=(select cantv_catalogo_detalle_id from cantv_pre_config_clasificador a '+ 
                           'inner join cantv_pre_nivel_clasificador b on a.id=b.cantv_pre_config_clasificador_id '+ 
                           'where a.id=%s and  b.id=%s) and nivel<(select b.nivel from cantv_pre_config_clasificador a '+ 
                           'inner join cantv_pre_nivel_clasificador b on a.id=b.cantv_pre_config_clasificador_id'+ 
                           'where a.id=%s and  b.id=%s)',())         
                
    

cantv_pre_clasificador_presupuestario()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: