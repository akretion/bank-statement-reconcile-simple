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

    def get_all_labels(self):
        dataset = super().get_all_labels()
        self._sale_order_get_all_labels(dataset)
        return dataset

    def _sale_order_get_all_labels(self, dataset):
        if self.sale_order_number_autocompletion:
            orders = self.env['sale.order'].search_read([
                ('company_id', '=', self.company_id.id),
                ('commercial_partner_id', '!=', False),
                ('state', '!=', 'cancel')],
                ['commercial_partner_id', 'name'])
            for order in orders:
                dataset[order['name'].upper()] = {
                    'partner_id': order['commercial_partner_id'][0]}
