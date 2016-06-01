# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_completion_label_simple for Odoo
#   Copyright (C) 2013-2016 Akretion (http://www.akretion.com)
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
from unidecode import unidecode
MEANINGFUL_PARTNER_NAME_MIN_SIZE = 3


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def update_partners(self):
        self.ensure_one()
        aslo = self.env['account.statement.label']
        dataset = aslo.get_all_labels()
        lines = self.env['account.bank.statement.line'].search([
            ('statement_id', '=', self.id), ('partner_id', '=', False)])
        for line in lines:
            line_name = line.name.upper()
            for stlabel in dataset:
                if aslo.match(line_name, stlabel[0]):
                    line.partner_id = stlabel[1]
                    break
        return True


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _complete_statement(self, stmts_vals, journal_id, account_number):
        '''Match the partner from the account.statement.label'''
        stmts_vals = super(AccountBankStatementImport, self).\
            _complete_statement(stmts_vals, journal_id, account_number)
        aslo = self.env['account.statement.label']
        dataset = aslo.get_all_labels()
        for line_vals in stmts_vals['transactions']:
            if not line_vals['partner_id']:
                line_name = line_vals['name'].upper()
                for stlabel in dataset:
                    if aslo.match(line_name, stlabel[0]):
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
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists in this company !'
        )]

    @api.model
    def match(self, bank_statement_line_name, label):
        if (
                ' ' + label + ' ' in bank_statement_line_name or
                bank_statement_line_name.startswith(label + ' ') or
                bank_statement_line_name.endswith(' ' + label) or
                label == bank_statement_line_name):
            return True
        else:
            return False

    @api.model
    def get_all_labels(self):
        self._cr.execute(
            """
            SELECT partner_id, label
            FROM account_statement_label
            WHERE company_id = %s OR company_id IS null
            """, (self.env.user.company_id.id,))
        dataset = [
            (r['label'].strip().upper(), r['partner_id'])
            for r in self._cr.dictfetchall()]
        self._cr.execute(
            """
            SELECT id, name FROM res_partner WHERE
            active IS true AND parent_id IS null
            AND (company_id = %s OR company_id IS null)
            """, (self.env.user.company_id.id,))
        for r in self._cr.dictfetchall():
            partner_name = unidecode(r['name'].strip().upper())
            if len(partner_name) >= MEANINGFUL_PARTNER_NAME_MIN_SIZE:
                dataset.append((partner_name, r['id']))
        # from pprint import pprint
        # pprint(dataset)
        return dataset


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_statement_label_ids = fields.One2many(
        'account.statement.label', 'partner_id',
        string='Bank Statement Labels')
