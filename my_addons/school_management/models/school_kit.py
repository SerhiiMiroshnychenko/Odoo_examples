from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


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


class SchoolStudent(models.Model):
    _name = 'school.student.student'
    _description = 'School_student model traditional prototype inheritance'
    _inherit = 'school.student.kit'

    teacher_ids = fields.Many2many(comodel_name='res.partner')


class SchoolInherited(models.Model):
    _inherit = 'school.student'

    friend_ids = fields.Many2many(
        comodel_name='school.student',
        relation='school_student_friend_rel',
        column1='student_id',
        column2='friend_id',
        string='Friends'
    )

    date_of_birth = fields.Date()
    age = fields.Integer(compute='_compute_age')
    admin_date = fields.Date(default=fields.Date.today())
    officer_id = fields.Many2one(
        comodel_name='res.users',
        string='Officer',
        default=lambda self: self.env.user)

    @api.depends('date_of_birth')
    def _compute_age(self):
        self.age = False
        for rec in self:
            rec.age = relativedelta(fields.Date.today(), rec.date_of_birth).years

    @api.constrains('date_of_birth', 'class_id')
    def validation_constrains(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth > today:
                raise ValidationError(_('Invalid Date of Birth'))
            if (rec.class_id > 12) or (rec.class_id < 1):
                raise ValidationError(_('Invalid Class'))

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
                raise ValidationError(_("Cannot add yourself as a friend."))

    def show_friends(self):
        for student in self:
            if student.friend_ids:
                friend_names = tuple([friend.name.name for friend in student.friend_ids])
                raise UserError(_(f"{student.name.name} has friends: {friend_names}"))
            raise UserError(_(f'{student.name.name} has no friends.'))

    def open_friends(self):
        context = {
            'default_friend_ids': [(6, 0, self.friend_ids.ids)]  # Passing friend IDs as a list
        }
        if self.friend_ids:
            return {
                'name': f'{self.name.name} has friends:',
                'res_model': 'school.student',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new',
                'view_id': self.env.ref('school_management.student_friends_view_form').id,
                'domain': [('id', '=', self.id)],
                'context': context
            }
        raise UserError(_(f'{self.name.name} has no friends.'))

    def see_friends(self):

        if self.friend_ids:
            return {
                'name': f'{self.name.name} has friends:',
                'res_model': 'school.student',
                'type': 'ir.actions.act_window',
                'view_mode': 'kanban',
                'target': 'new',
                'view_id': self.env.ref('school_management.student_friends_view_kanban').id,
                'domain': [('id', 'in', self.friend_ids.ids)],
            }
        raise UserError(_(f'{self.name.name} has no friends.'))
