from odoo import models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    # Constants for administrative fees and tax rate
    ADMINISTRATIVE_FEES = 100.00
    TAX_RATE = 0.06  # 6% of the selling price
    CUSTOMER_INV = 'Journal Name'

    def action_set_sold_status(self):
        """
        Метод встановлює статус нерухомості як "sold" і створює рахунок-фактуру для продажу.

        :return: результат виконання оригінального методу
        """
        result = super(EstateProperty, self).action_set_sold_status()

        print(f'{self.title} is sold! (In Estate Account)')

        # Знаходимо журнал "Customer Invoices" для використання в рахунку-фактурі
        journal = self._get_customer_invoices_journal()
        invoice = self._create_customer_invoice(journal)
        self._create_invoice_lines(invoice)

        return result

    def _get_customer_invoices_journal(self):
        """
        Повертає журнал "Customer Invoices", якщо він існує, або піднімає виключення UserError.

        :return: журнал "Customer Invoices"
        """
        if journal := self.env['account.journal'].search(
            [('type', '=', 'sale')], limit=1
        ):
            return journal
        else:
            # Якщо журнал не існує
            raise UserError(
                "The 'Customer Invoices' journal is not found. Please create the journal before selling properties.")

    def _create_customer_invoice(self, journal):
        """
        Створює рахунок-фактуру для покупця.

        :param journal: журнал для рахунку-фактури
        :return: створений рахунок-фактура
        """
        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        print(f'{invoice=}')
        return invoice

    def _create_invoice_lines(self, invoice):
        """
        Створює рядки рахунку-фактури для проданої властивості.

        :param invoice: створений рахунок-фактура
        :return: None
        """
        lines_to_create = []
        for estate in self:
            if estate.state == 'sold' and estate.selling_price and estate.selling_price > 0:
                # Розраховуємо додаткові рядки рахунку-фактури
                tax_amount = estate.selling_price * self.TAX_RATE

                lines_to_create.extend(
                    (
                        {
                            'move_id': invoice.id,
                            'name': 'Selling Price',
                            'quantity': 1,
                            'price_unit': estate.selling_price,
                        },
                        {
                            'move_id': invoice.id,
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': self.ADMINISTRATIVE_FEES,
                        },
                        {
                            'move_id': invoice.id,
                            'name': 'Tax',
                            'quantity': 1,
                            'price_unit': tax_amount,
                        },
                    )
                )
        # Створюємо рядки рахунку-фактури
        self.env['account.move.line'].create(lines_to_create)

