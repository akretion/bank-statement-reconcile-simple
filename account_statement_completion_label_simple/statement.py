# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_completion_label_simple for Odoo
#   Copyright (C) 2013-2015 Akretion (http://www.akretion.com)
#   @author Benoît GUILLOT <benoit.guillot@akretion.com>
#   @author Alexis de LATTRE <alexis.delattre@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import fields, models, api


class AccountBankSatement(models.Model):
    """We add a basic button and stuff to support the auto-completion
    of the bank statement once line have been imported or manually fullfill.
    """
    _inherit = "account.bank.statement"

    @api.multi
    def go_to_completion_label(self):
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account_statement_completion_label_simple',
            'statement_label_action')
        return action


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _complete_statement(self, stmts_vals, journal_id, account_number):
        '''Match the partner from the account.statement.label'''
        stmts_vals = super(AccountBankStatementImport, self).\
            _complete_statement(stmts_vals, journal_id, account_number)
        self._cr.execute(
            """
            SELECT partner_id, label
            FROM account_statement_label
            WHERE company_id = %s OR company_id IS null
            """, (self.env.user.company_id.id,))
        dataset = [
            (r['label'].upper(), r['partner_id'])
            for r in self._cr.dictfetchall()]
        for line_vals in stmts_vals['transactions']:
            if not line_vals['partner_id']:
                for stlabel in dataset:
                    if stlabel[0] in line_vals['name'].upper():
                        line_vals['partner_id'] = stlabel[1]
                        break
        return stmts_vals


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Account Statement Label"

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)])
    label = fields.Char('Bank Statement Label', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'account.statement.label'))

    _sql_constraints = [(
        'label_company_unique', 'unique (label, company_id)',
        'This label already exists in this company !'
        )]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_statement_label_ids = fields.One2many(
        'account.statement.label', 'partner_id',
        string='Bank Statement Labels')
