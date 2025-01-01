# Copyright 2013-2024 Akretion France (https://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_statement_label_ids = fields.One2many(
        'account.statement.label', 'partner_id',
        string='Bank Statement Labels')
    bank_statement_label_count = fields.Integer(
        compute='_compute_bank_statement_label_count',
        string='Number of Bank Statement Labels')

    def _compute_bank_statement_label_count(self):
        label_data = self.env['account.statement.label']._read_group(
            [('partner_id', 'in', self.ids)], groupby=['partner_id'], aggregates=['__count'])
        mapped_data = {partner.id: lb_count for (partner, lb_count) in label_data}
        for partner in self:
            partner.bank_statement_label_count = mapped_data.get(partner.id, 0)
