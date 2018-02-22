# -*- coding: utf-8 -*-
from odoo import api, models


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

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
