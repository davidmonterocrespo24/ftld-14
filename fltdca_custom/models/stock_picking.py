# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_send_tracking_no(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        delivery_template_id = self.env.ref('stock.mail_template_data_delivery_confirmation').id
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'stock.picking',
            # 'default_res_id': self.sale_id.id if self.sale_id else False,
            'default_res_id': self.id,
            'default_use_template': bool(delivery_template_id),
            'default_template_id': delivery_template_id,
            'default_composition_mode': 'comment',
            # 'mark_so_as_sent': True,
            'custom_layout':'mail.mail_notification_light',
            # 'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

