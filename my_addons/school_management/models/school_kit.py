from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SchoolKit(models.Model):
    _name = 'school.student.kit'
    _description = 'School_student model delegate inheritance'
    _inherits = {'school.student': 'student_id'}

    student_id = fields.Many2one(
        comodel_name='school.student',
        string='Related_student_id',
        auto_join=True, index=True,
        ondelete="cascade",
        required=True
    )

    major = fields.Char()


class SchoolInherited(models.Model):
    _inherit = 'school.student'

    friend_ids = fields.Many2many(
        comodel_name='school.student',
        relation='school_student_friend_rel',
        column1='student_id',
        column2='friend_id',
        string='Friends'
    )

    @api.onchange('friend_ids')
    def _set_friends(self):
        # SELF - тимчасовий об'єкт, що зберігається тільки в пам'яті. Має NewId
        # SELF_OBJECT - отримуємо постійний об'єкт з ID рівним чисельному значенню 'NewId' об'єкта SELF
        self_object = self.env['school.student'].search([('id', '=', self.id.origin)])
        friends = self.env['school.student'].search([('id', 'in', self.friend_ids.ids)])
        for friend in friends:
            friend.friend_ids |= self_object

        not_friends = self.env['school.student'].search([('id', 'not in', self.friend_ids.ids)])
        for not_friend in not_friends:
            not_friend.friend_ids -= self_object

    @api.constrains('friend_ids')
    def _check_friend_ids(self):
        for student in self:
            if student in student.friend_ids:
                raise ValidationError("Cannot add yourself as a friend.")

    # def write(self, vals):
    #     print(f'Before super(): {vals=}')
    #     vals = {'friend_ids': [[6, False, [13, 14]]]}
    #     if 'friend_ids' in vals:
    #         friends = vals['friend_ids'][0][-1]
    #         print(f'{friends=}')
    #
    #     result = super().write(vals)
    #     print(f'After super(): {vals=}')
    #
    #     return result

    def show_friends(self):
        print(f'"{self.name.name}"({self.id}) has friends: {[friend.name.name for friend in self.friend_ids]}')
