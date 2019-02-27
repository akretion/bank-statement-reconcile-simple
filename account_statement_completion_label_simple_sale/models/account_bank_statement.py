# Copyright 2018-2019 Akretion France (http://www.akretion.com)
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.model
    def get_all_labels(self, journal):
        dataset = super(AccountBankStatement, self).get_all_labels(journal)
        if journal.sale_order_number_autocompletion:
            orders = self.env['sale.order'].search_read([
                ('state', '!=', 'cancel')],
                ['commercial_partner_id', 'name'])
            for order in orders:
                dataset.append((
                    order['name'].upper(),
                    order['commercial_partner_id'][0],
                    False))
        return dataset
