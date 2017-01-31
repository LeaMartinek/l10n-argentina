# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012-2014 E-MIPS (http://www.e-mips.com.ar)
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

from osv import osv, fields
from tools.translate import _
import time

class sale_shop(osv.osv):
    _name = "sale.shop"
    _inherit = "sale.shop"
    _columns = {
        #'pos_ar_ids' : fields.one2many('pos.ar','shop_id','Points of Sales'),
        'pos_ar_ids' : fields.many2many('pos.ar','sale_shop_pos_ar_rel', 'shop_id', 'pos_ar_id' ,'Points of Sales'),
    }
sale_shop()

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_pos_ar(self, cr, uid, order, denom_id, context=None):

        pos_ar_obj = self.pool.get('pos.ar')
        
        if not order.fiscal_position :
            raise osv.except_osv( _('Error'),
                                  _('Check the Fiscal Position Configuration')) 
        
        possible_pos = [pos.id for pos in order.shop_id.pos_ar_ids]
        res_pos = pos_ar_obj.search(cr, uid,[('id', 'in', possible_pos), ('denomination_id', '=', denom_id)], order="priority asc")
        if not len(res_pos):
            raise osv.except_osv( _('Error'),
                                  _('You need to set up a Shop and/or a Fiscal Position')) 
 
        return res_pos[0]

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = super(sale_order, self)._prepare_invoice(
            cr, uid, order, lines, context=context)

        if not order.fiscal_position:
            raise osv.except_osv(_("Sale Error"),
                    _("You have to set up Fiscal Position in this Order."))

        denom_id = order.fiscal_position.denomination_id
        pos_ar_id = self._get_pos_ar(cr, uid, order, denom_id.id, context=context)
                                 
        invoice_vals.update({'denomination_id' : denom_id.id ,
                             'pos_ar_id': pos_ar_id })

        return invoice_vals

    def action_wait(self, cr, uid, ids, *args):
        for o in self.browse(cr, uid, ids):
            if not o.fiscal_position:
                #TODO poner esto en un log:
                print 'Error - No Fiscal Position Setting. Please set the Fiscal Position First'
                #~ raise osv.except_osv(   _('No Fiscal Position Setting'),
                                        #~ _('Please set the Fiscal Position First'))
            if (o.order_policy == 'manual'):
                self.write(cr, uid, [o.id], {'state': 'manual', 'date_confirm': time.strftime('%Y-%m-%d')})
            else:
                self.write(cr, uid, [o.id], {'state': 'progress', 'date_confirm': time.strftime('%Y-%m-%d')})
            self.pool.get('sale.order.line').button_confirm(cr, uid, [x.id for x in o.order_line])
#            message = _("The quotation '%s' has been converted to a sales order.") % (o.name,)
#            self.log(cr, uid, o.id, message)
        return True

    
sale_order()
