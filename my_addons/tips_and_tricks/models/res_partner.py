from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        """
        Дозволяє вести пошук партнера не тільки за ім'ям,
        але і за телефоном та поштою
        :param name: Параметр, який вводить користувач
        :param args: Додаткові аргументи
        :param operator: Оператор, що використовується в домені пошуку
        :param limit: Ліміт на результати пошуку
        :param name_get_uid: Додатковий ідентифікатор користувача для використання під час перевірки прав доступу
        :return: Список ідентифікаторів записів або ціле число (якщо count має значення True)
        """
        args = args or []
        domain = []
        if name:
            domain = ['|', '|',
                      ('name', operator, name),
                      ('phone', operator, name),
                      ('email', operator, name)
                      ]
        return self._search(domain + args,
                            limit=limit,
                            access_rights_uid=name_get_uid)
