# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_statement_label_ids = fields.One2many(
        'account.statement.label', 'partner_id',
        string='Bank Statement Labels')
    bank_statement_label_count = fields.Integer(
        compute='_compute_bank_statement_label_count',
        string='Number of Bank Statement Labels')

    def _compute_bank_statement_label_count(self):
        label_data = self.env['account.statement.label'].read_group(
            [('partner_id', 'in', self.ids)], ['partner_id'], ['partner_id'])
        mapped_data = dict([
            (label['partner_id'][0], label['partner_id_count'])
            for label in label_data])
        for partner in self:
            partner.bank_statement_label_count = mapped_data.get(partner.id, 0)
