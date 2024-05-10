from json import dumps

from odoo import fields, models


class FishInformation(models.TransientModel):
    _name = 'fish.information'
    _description = 'Fish Information'

    fish_id = fields.Integer()
    json_fish_info = fields.Char(compute='_compute_json_fish_info')
    html_fish_info = fields.Char(compute='_compute_html_fish_info')

    def _compute_json_fish_info(self):
        fish = self.env['fish.fish'].browse(self.fish_id)
        fish_info = {
            'name': f'{fish.common_name} ({fish.scientific_name})',
            'size': fish.average_size,
        }
        self.json_fish_info = dumps({
            'template': 'fish.fishFishes',
            'fish_info': fish_info,
        })

    def _compute_html_fish_info(self):
        fish = self.env['fish.fish'].browse(self.fish_id)
        fish_info = f'''
        <div id="demo"
        style="color: red; text-align: center; font-size: 16px;
        transition: color 0.3s ease;"
        onmouseover="this.style.color='green';
        this.style.fontWeight='bold';"
        onmouseout="this.style.color='red';
        this.style.fontWeight='normal';
        ">
        <h2>{fish.common_name}</h2>
        <hr/>
        <p><i>({fish.scientific_name})</i></p>
        <p><b>{fish.average_size}</b> mm</p><div>
'''
        self.html_fish_info = fish_info
