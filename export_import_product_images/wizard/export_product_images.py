# -*- coding: utf-8 -*-
import base64, zipfile, os
from io import BytesIO
from odoo import api, fields, models, _
import os
import base64
import zipfile
from odoo.exceptions import UserError, ValidationError
import csv




class export_product_images(models.TransientModel):
    _name = "export.product.images"
    _description = "Save Product Image to a Particular Folder"
    location = fields.Char(string="Location", help='Path to Save the Product Images')
    image_size = fields.Selection(string='Image Size',
                                  selection=[('image', 'Large'), ('image_medium', 'Medium'), ('image_small', 'Small')],
                                  default='image',
                                  help=" Large Image is Limited to Maximum 1024x1024px, Medium is a 128x128px image and Small is a 64x64px image")

    # @api.multi
    # def export_images(self):
    #     current = self
    #     product_ids = self._context.get('active_ids') or []
    #     if not os.path.exists(current.location):
    #         raise UserError(("Specified Location %s does not Exist.") % (current.location))
    #     elif not os.path.isdir(current.location):
    #         raise UserError(("Specified Location %s is not a Directory.") % (current.location))
    #     elif not os.access(current.location, os.W_OK):
    #         raise UserError(("Specified Location %s does not have Write Access.") % (current.location))
    #     data = ('name', 'image')
    #
    #     for user in self.env['product.template'].browse(product_ids):
    #         try:
    #             img = current.image_size == 'image' and user.image or (
    #                         current.image_size == 'image_medium' and user.image_medium or user.image_small)
    #             if img:
    #                 user_img = base64.b64decode(img)
    #                 file_name = user.name+ '.jpg'
    #                 with open(os.path.join(current.location, file_name.replace('/', ' ')), 'wb') as f:
    #                     f.write(user_img)
    #                     f.close()
    #
    #         except:
    #             continue
    #
    #     return True


    def export_images(self):
        current = self
        product_ids = self._context.get('active_ids') or []
        tmp = '/tmp/odoo/image_product_export/'
        tmp= os.path.join(tmp,'image_product_export')
        if not os.path.exists(tmp):
            try:
                os.makedirs(tmp)
            except Exception as ex:
                print(ex)
        zip_base64 = BytesIO()
        zip_file = zipfile.ZipFile(zip_base64, 'w')
        for product in self.env['product.template'].browse(product_ids):
            try:
                img = current.image_size == 'image' and product.image or (
                        current.image_size == 'image_medium' and product.image_medium or product.image_small)
                if img:
                    user_img = base64.b64decode(img)
                    file_name = os.path.join(tmp,product.name + '.jpg')
                    with open(file_name, 'wb') as f:
                        f.write(user_img)
                        f.close()
                    zip_file.write(file_name, product['name'])
            except Exception as ex:
                print(ex)

        zip_file.close()
        zip_base64.seek(0)
        return base64.b64encode(zip_base64.getvalue())

    def export_adjuntos(self):
        tmp = '/tmp/odoo/attachment_export/'
        tmp= os.path.join(tmp,'attachment_export')
        if not os.path.exists(tmp):
            try:
                os.makedirs(tmp)
            except Exception as ex:
                print(ex)
        zip_base64 = BytesIO()
        zip_file = zipfile.ZipFile(zip_base64, 'w')
        for attachment in self.env['ir.attachment'].search([('res_model','=',self.location)]):
            try:
                att = attachment.datas
                if att:
                    user_img = base64.b64decode(att)
                    file_name = os.path.join(tmp,attachment.name)
                    with open(file_name, 'wb') as f:
                        f.write(user_img)
                        f.close()
                    zip_file.write(file_name,attachment.name)
            except Exception as ex:
                print(ex)

        zip_file.close()
        zip_base64.seek(0)
        return base64.b64encode(zip_base64.getvalue())
