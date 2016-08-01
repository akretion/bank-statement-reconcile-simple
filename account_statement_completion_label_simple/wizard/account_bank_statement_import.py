# -*- coding: utf-8 -*-
from openerp import api, models


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def _import_statement(self, stmt_vals):
        statement_id, notif = super(AccountBankStatementImport, self).\
            _import_statement(stmt_vals)
        statement_obj = self.env['account.bank.statement']
        statement = statement_obj.browse(statement_id)
        if statement.journal_id.automate_entry:
            statement.create_line_entries_from_account()
        return statement_id, notif
