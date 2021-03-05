# Copyright 2013-2019 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    # def create_line_entries_from_account(self):
    #    for stmt in self:
    #        st_lines = self.env['account.bank.statement.line'].search([
    #            ('statement_id', '=', stmt.id),
    #            ('account_id', '!=', False),
    #            ('move_id', '=', False),
    #            ])
    #        st_lines.fast_counterpart_creation()

    def update_statement_lines(self):
        self.ensure_one()
        dataset = self.journal_id.get_all_labels()
        if dataset:
            lines = self.env['account.bank.statement.line'].search([
                ('statement_id', '=', self.id),
                ('partner_id', '=', False),
                # ('account_id', '=', False),
                ('move_id.state', '!=', 'posted'),
                ])
            for line in lines:
                line_pay_ref = line.payment_ref.upper()
                for stlabel in dataset:
                    if self.match(line_pay_ref, stlabel[0]):
                        lvals = {'partner_id': stlabel[1]}
                        if stlabel[2]:
                            lvals['account_id'] = stlabel[2]
                        line.write(lvals)
                        break
        # if self.journal_id.automate_entry:
        #    self.create_line_entries_from_account()

    @api.model
    def match(self, bank_statement_line_pay_ref, label):
        if label in bank_statement_line_pay_ref:
            return True
        else:
            return False

    def button_post(self):
        super().button_post()
        account_st_lines = self.line_ids.filtered(lambda l: l.account_id)
        for st_line in account_st_lines:
            liquidity_lines, suspense_lines, other_lines = st_line._seek_for_lines()
            (suspense_lines + other_lines).write({
                'account_id': st_line.account_id.id,
            })
        account_st_lines._compute_is_reconciled()


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    account_id = fields.Many2one('account.account')

#    def _synchronize_to_moves(self, changed_fields):
#        super()._synchronize_to_moves(changed_fields)
#        if 'account_id' not in changed_fields:
#            return
#        for st_line in self.with_context(skip_account_move_synchronization=True):
#            liquidity_lines, suspense_lines, other_lines = st_line._seek_for_lines()
#            account = st_line.account_id
#            if account:
#                (suspense_lines + other_lines).write({
#                    'account_id': account.id
#                })
#            else:
#                (suspense_lines + other_lines).write({
#                    "account_id": st_line.journal_id.suspense_account_id.id
#                })
