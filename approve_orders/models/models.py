# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


# class approve_orders(models.Model):
#     _name = 'approve_orders.approve_orders'
#     _description = 'approve_orders.approve_orders'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class OrderHeader(models.Model):
    _name = 'approve_orders.order_header'
    _description = 'approve_orders.order_header'

    order_type_id = fields.Many2one('vcsgroup.booking', string="Order Type", required=True)
    order_date = fields.Date(
        string="Date", default=lambda self: fields.Date.today())
    name = fields.Char(size=15, string="Order No.")
    partner_id = fields.Many2one("res.partner", string="Partner")
    item_count = fields.Integer(string="Item", default="0")
    vat_total = fields.Float(string="Vat.", default="0.0")
    order_step = fields.Many2one(
        'vcsgroup.order_step', string="Step", default="None")
    remark = fields.Text(string="Remark", default="-")
    is_approve = fields.Selection([("0", "Open"), ("1", "In Process"), (
        "2", "Approved"), ("3", "Completed"), ("4", "Cancel")], string="Status", default="0")
    is_sync = fields.Boolean(string="Is Sync", default=False)
    line_ids = fields.One2many(
        "approve_orders.order_detail", "order_id", string="Order Detail")
    

    # @api.multi
    # def btn_show_dialog_box(self):
    #     text = """Write your custom message here to show in dialog box"""
    #     query ='delete from display_dialog_box'
    #     self.env.cr.execute(query)
    #     value = self.env['display.dialog.box'].sudo().create({'text':text})
    #     return{
    #         'type':'ir.actions.act_window',
    #         'name':'Message',
    #         'res_model':'display.dialog.box',
    #         'view_type':'form',
    #         'view_mode':'form',
    #         'target':'new',
    #         'res_id':value.id                
    #     }

    @api.model
    def create(self, data):
        dte = datetime.strptime(data['order_date'], '%Y-%m-%d')
        ctnRecord = self.env['approve_orders.order_header'].search_count([('name', 'like', f"ORD{dte.strftime('%Y%m')[3:]}")]) 
        orderNo = f"ORD{dte.strftime('%Y%m')[3:]}{'{0:05}'.format(ctnRecord + 1)}"
        data['name'] = orderNo
        data['item_count'] = len(data['line_ids'])
        data['order_step'] = 1
        data['is_approve'] = "0"
        result = super().create(data)
        return result
    
    @api.onchange('line_ids')
    def onchange_line_ids(self):
        _id = []
        vatCount = 0
        for r in self.line_ids:
            vatCount += float(r['product_id']['price'])
            if len(_id) > 0:
                try:
                    if _id.index(r['product_id']['id']):
                        raise ValidationError(str('Product duplicate!'))
                    
                    print(f"Found Duplicate: {_id.index(r['product_id']['id'])}")

                except ValueError:
                    pass
            
            _id.append(r['product_id']['id'])

        print(_id)
        self.vat_total = vatCount
        self.item_count = len(self.line_ids)
        # self.line_ids = docs

    # @api.ondelete(self)
    # def ondelete_order_header(self):
    #     # self.line_ids.unlink()
    #     pass

    def btn_approve(self):
        print(f"btn click to approve")



class OrderDetail(models.Model):
    _name = 'approve_orders.order_detail'
    _description = 'approve_orders.order_detail'

    order_id = fields.Many2one('approve_orders.order_header', string="Order")
    product_id = fields.Many2one('vcsgroup.product_group', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default="1.0", required=True)
    price = fields.Float(string="Price", default="0.0")
    unit_id = fields.Many2one('vcsgroup.unit', string="Unit", required=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.price = float(self.product_id.price)
        print(f"Change product_id: {self.product_id.id}")
