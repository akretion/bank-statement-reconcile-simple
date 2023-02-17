# Copyright 2018-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountStatementLabelCreate(models.TransientModel):
    _name = 'account.statement.label.create'
    _description = 'Account Statement Label Create Wizard'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert self._context.get('active_model') ==\
            'account.bank.statement.line', 'Wrong active model'
        assert self._context.get('active_id'), 'missing active_id in context'
        line = self.env['account.bank.statement.line'].browse(
            self._context['active_id'])
        res.update({
            'new_label': line.payment_ref,
            'statement_line_id': line.id,
            'company_id': line.company_id.id,
        })
        return res

    statement_line_id = fields.Many2one(
        'account.bank.statement.line', string='Bank Statement Line',
        readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)
    current_label = fields.Char(
        related='statement_line_id.payment_ref', readonly=True,
        string='Statement Line Label')
    new_label = fields.Char(string="New Label", required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner',
        domain="[('parent_id', '=', False), ('company_id', 'in', (False, company_id))]")
    counterpart_account_id = fields.Many2one(
        'account.account', 'Counterpart Account',
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]")

    def run(self):
        self.ensure_one()
        self.env['account.statement.label'].create({
            'label': self.new_label.strip(),
            'company_id': self.statement_line_id.company_id.id,
            'partner_id': self.partner_id.id or False,
            'counterpart_account_id': self.counterpart_account_id.id or False,
        })
        self.statement_line_id.update_statement_lines()
