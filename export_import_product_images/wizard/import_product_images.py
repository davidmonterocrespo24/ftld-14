# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import base64, zipfile, os
from io import BytesIO
from odoo.tools.osutil import tempdir
import logging
_logger = logging.getLogger(__name__)
MAX_FILE_SIZE = 100 * 1024 * 1024  # in megabytes
import base64
from odoo.exceptions import UserError, ValidationError
import csv
import zipfile
import os
import base64
import base64
from io import StringIO  ## for Python 3
import sys
from os import listdir


class import_user_images(models.TransientModel):
    _name = "import.product.images"
    _description = "Save Product Image to a Particular Folder"
    file = fields.Binary(u'Zip File', required=True)


    def import_images(self):
        self.ensure_one()
        zip_data = base64.decodebytes(self.module_file)
        fp = BytesIO()
        fp.write(zip_data)

        if not fp:
            _logger.error(_("No file sent.................................."))
            raise Exception(_("No file sent."))
        if not zipfile.is_zipfile(fp):
            raise UserError(_('Only zip files are supported.'))

        with zipfile.ZipFile(fp, "r") as z:
            for zf in z.filelist:
                if zf.file_size > MAX_FILE_SIZE:
                    _logger.error(_("File '%s' exceed maximum allowed file size") % zf.filename)
                    raise UserError(_("File '%s' exceed maximum allowed file size") % zf.filename)

                (name, extension) = os.path.splitext(zf.filename)
                name=name
                if extension in ['JPG','jpg','PNG','png']:
                    product_ids = self.env['product.template'].search([('name', '=', name)])
                    if product_ids:
                        _logger.error(_("Product  '%s'...................................") % product_ids[0].name)
                        product_id = product_ids[0]
                        data = z.read(zf.filename)

                        product_id.image = base64.b64encode(data)
                    else:
                        _logger.error(_("Noooo   Product  '%s'...................................") % product_ids[0].name)