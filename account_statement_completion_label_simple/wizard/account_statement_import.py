# Copyright 2013-2019 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountStatementImport(models.TransientModel):
    _inherit = 'account.statement.import'

    def _complete_stmts_vals(self, stmts_vals, journal, account_number):
        '''Match the partner from the account.statement.label'''
        stmts_vals = super()._complete_stmts_vals(stmts_vals, journal, account_number)
        abso = self.env['account.bank.statement']
        dataset = journal.get_all_labels()
        if dataset:
            for st_vals in stmts_vals:
                for lvals in st_vals['transactions']:
                    if not lvals.get('partner_id'):
                        line_pref = lvals['payment_ref'].upper()
                        for stlabel in dataset:
                            if abso.match(line_pref, stlabel[0]):
                                lvals['partner_id'] = stlabel[1]
                                if stlabel[2]:
                                    lvals['counterpart_account_id'] = stlabel[2]
                                break
        return stmts_vals
