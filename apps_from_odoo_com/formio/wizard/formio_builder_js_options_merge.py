# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from odoo import api, fields, models

from ..utils import json_loads


class BuilderJsOptionsMerge(models.TransientModel):
    _name = 'formio.builder.js.options.merge'
    _description = "Form Builder JS Options Merge"

    formio_js_options_current_id = fields.Many2one(
        comodel_name='formio.builder.js.options',
        string='Source Options Record',
        required=True
    )
    formio_js_options_current = fields.Text(
        string='formio.js JS Options Current',
        related='formio_js_options_current_id.value'
    )
    formio_js_options_merge_id = fields.Many2one(
        comodel_name='formio.builder.js.options',
        string='Merge Options Record',
        default=lambda self: self._default_js_options_merge_id(),
        domain="[('id', '!=', formio_js_options_current_id)]",
        required=True
    )
    formio_js_options_merge = fields.Text(
        string='formio.js JS Options Merge',
        related='formio_js_options_merge_id.value'
    )
    formio_js_options_merge_preview = fields.Text(
        string='formio.js JS Options Preview',
        compute='_compute_js_options_merge_preview'
    )

    def _default_js_options_merge_id(self):
        Param = self.env['ir.config_parameter'].sudo()
        default_builder_js_options_id = Param.get_param(
            'formio.default_builder_js_options_id'
        )
        options = self.env['formio.builder.js.options'].browse(
            int(default_builder_js_options_id)
        )
        if options:
            return options.id
        else:
            return False

    def action_merge(self):
        self.ensure_one()
        self._compute_js_options_merge_preview()
        self.formio_js_options_current_id.write({
            'value': self.formio_js_options_merge_preview
        })

    @api.depends('formio_js_options_merge')
    def _compute_js_options_merge_preview(self):
        self.ensure_one()
        if self.formio_js_options_merge:
            merged = self._merge_js_options()
            self.formio_js_options_merge_preview = json.dumps(merged, indent=4)
        else:
            self.formio_js_options_merge_preview = False

    def _merge_js_options(self):
        formio_js_options_current = json_loads(self.formio_js_options_current)
        formio_js_options_merge = json_loads(self.formio_js_options_merge)
        merged = self._recursive_merge_js_options(
            formio_js_options_merge, formio_js_options_current
        )
        return merged

    @classmethod
    def _recursive_merge_js_options(cls, dict1, dict2):
        """ Merge dict1 into dict2 (keep data for dict2 keys) """
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                dict1[key] = cls._recursive_merge_js_options(dict1[key], value)
            else:
                # Merge non-dictionary values
                dict1[key] = value
        return dict1
