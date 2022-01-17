from odoo import fields, models, api


class WooProductTemplateEpt(models.Model):
    _inherit = "woo.product.template.ept"


    def prepare_product_update_data(self, template, update_image, update_basic_detail, data):

        instance = template.woo_instance_id
        flag = False
        tmpl_images = []
        if update_image:
            tmpl_images += self.get_gallery_images(instance, template, template.product_tmpl_id)
            data.update({"images": tmpl_images})
            flag = True

        if update_basic_detail:
            weight = self.convert_weight_by_uom(template.product_tmpl_id.weight, instance)

            description = template.with_context(lang=instance.woo_lang_id.code).woo_description
            short_description = template.with_context(lang=instance.woo_lang_id.code).woo_short_description

            data.update({
                'name': template.name,
                'enable_html_description': True,
                'enable_html_short_description': True, 'description': description,
                'short_description': short_description,
                'weight': str(weight),
                'taxable': template.taxable and 'true' or 'false',
                'brand': 3
            })
            data = template.add_woo_category_and_tags(data)

        return flag, data