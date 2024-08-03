# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BuilderJsOptions(models.Model):
    _name = 'formio.builder.js.options'
    _description = 'formio.builder JavaScript Options'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name ASC'

    name = fields.Char(string='Name', required=True)
    value = fields.Text(
        string='Value (JSON)',
        default=lambda self: self._default_options_value(),
        tracking=True
    )

    @api.constrains('value')
    def _constraint_value(self):
        for rec in self:
            if not rec.value:
                msg = _(
                    'Value is required and must contain at least empty JSON: {}'
                )
                raise ValidationError(msg)

    @api.model
    def _default_options_value(self):
        Param = self.env['ir.config_parameter'].sudo()
        default_builder_js_options_id = Param.get_param(
            'formio.default_builder_js_options_id'
        )
        options = self.env['formio.builder.js.options'].browse(
            int(default_builder_js_options_id)
        )
        if options:
            return options.value
        else:
            return False
