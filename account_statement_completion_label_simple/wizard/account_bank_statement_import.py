# Copyright 2013-2019 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def _complete_stmts_vals(self, stmts_vals, journal, account_number):
        '''Match the partner from the account.statement.label'''
        stmts_vals = super(AccountBankStatementImport, self).\
            _complete_stmts_vals(stmts_vals, journal, account_number)
        abso = self.env['account.bank.statement']
        dataset = abso.get_all_labels(journal)
        if dataset:
            for st_vals in stmts_vals:
                for line_vals in st_vals['transactions']:
                    if not line_vals.get('partner_id'):
                        line_name = line_vals['name'].upper()
                        for stlabel in dataset:
                            if abso.match(line_name, stlabel[0]):
                                line_vals['partner_id'] = stlabel[1]
                                if stlabel[2]:
                                    line_vals['account_id'] = stlabel[2]
                                break
        return stmts_vals

    @api.model
    def _create_bank_statements(self, stmts_vals):
        statement_ids, notifs = super(AccountBankStatementImport, self).\
            _create_bank_statements(stmts_vals)
        statement_obj = self.env['account.bank.statement']
        statements = statement_obj.browse(statement_ids)
        for statement in statements:
            if statement.journal_id.automate_entry:
                statement.create_line_entries_from_account()
        return statement_ids, notifs
