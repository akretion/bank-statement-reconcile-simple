# Copyright 2013-2019 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _complete_stmts_vals(self, stmts_vals, journal, account_number):
        '''Match the partner from the account.statement.label'''
        stmts_vals = super()._complete_stmts_vals(stmts_vals, journal, account_number)
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

    def _create_bank_statements(self, stmts_vals):
        statement_line_ids, notifs = super()._create_bank_statements(stmts_vals)
        abslo = self.env['account.bank.statement.line']
        lines = abslo.browse(statement_line_ids)
        for line in lines.filtered(
                lambda x: x.account_id and
                not x.journal_entry_ids and
                x.statement_id.journal_id.automate_entry):
            line.fast_counterpart_creation()
        return statement_line_ids, notifs
