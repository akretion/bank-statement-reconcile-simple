# Copyright 2018-2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    sale_order_number_autocompletion = fields.Boolean(
        string="Sale Order Number Completion",
        default=True,
        help="If enabled, the partner field of bank statement "
        "lines will be automatically set if it contains a sale "
        "order number.")

    def _get_sale_order_domain(self):
        return [
                ('company_id', '=', self.env.company.id),
                ('commercial_partner_id', '!=', False),
                ('state', '!=', 'cancel'),
        ]

    def _get_sale_order_read_fields(self):
        return ['commercial_partner_id', 'name']

    def _get_dataset_from_sale_order(self, order):
        return (
            order['name'].upper(),
            order['commercial_partner_id'][0],
        )

    def get_all_labels(self):
        dataset = super().get_all_labels()
        if self.sale_order_number_autocompletion:
            orders = self.env['sale.order'].search_read(
                self._get_sale_order_domain(),
                self._get_sale_order_read_fields()
            )
            for order in orders:
                dataset.append(self._get_dataset_from_sale_order(order))
        return dataset
