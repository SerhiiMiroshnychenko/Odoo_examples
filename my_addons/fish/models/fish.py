from odoo import fields, models


class FishFish(models.Model):
    _name = 'fish.fish'
    _description = 'Fish model'

    common_name = fields.Char(required=True)
    scientific_name = fields.Char()
    average_size = fields.Integer(string='Average size, mm')
    image = fields.Image()
    remarks = fields.Html()
    info_id = fields.Integer()

    def info(self):
        vals_list = {
            'fish_id': self.id
        }
        fish_info = self.env['fish.information'].create(vals_list)
        view_id = self.env.ref('fish.view_fish_info').id
        action = {
            'type': 'ir.actions.act_window',
            'res_id': fish_info.id,
            'res_model': 'fish.information',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
        }
        return action

    def remark(self):
        cr = self.env.cr
        query = f"""SELECT remarks FROM fish_fish WHERE id={self.id}"""
        cr.execute(query)
        result = cr.fetchall()
        view_name = 'fish_remark_popup'
        view = self.env['ir.ui.view'].search([('name', '=', view_name)])
        if not view:
            view = self.env['ir.ui.view'].create({
                'name': 'fish_remark_popup',
                'type': 'form',
                'model': 'fish.fish',
                'arch': """
                                <form>
                                    <sheet>
                                        <field name="remarks" widget="html" />
                                    </sheet>
                                </form>
                            """,
            })
        return {
            'name': self.common_name,
            'type': 'ir.actions.act_window',
            'res_model': 'fish.fish',
            'view_mode': 'form',
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'context': {'default_remarks': result},
        }

