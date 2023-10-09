# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# @author: Florian da Costa <florian.dacosta@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def update_statement_lines(self):
        """Method called by the button on bank statement form view"""
        self.ensure_one()
        dataset = self.journal_id.get_all_labels()
        if dataset:
            lines = self.env['account.bank.statement.line'].search([
                ('statement_id', '=', self.id),
                ('is_reconciled', '=', False),
                ])
            updated_lines = {}
            for line in lines:
                line_pay_ref = line.payment_ref.upper()
                for label, data in dataset.items():
                    if self.match(line_pay_ref, label):
                        if data.get('partner_id') and not line.partner_id:
                            lvals = {'partner_id': data['partner_id']}
                            line.write(lvals)
                            updated_lines[line.id] = True
                        if data.get('account_id'):
                            line.move_id.line_ids.with_context(
                                force_delete=True).unlink()
                            mvals = {'line_ids': [
                                (0, 0, x) for x
                                in line._prepare_move_line_default_vals(
                                    counterpart_account_id={
                                        'account_id': data['account_id'],
                                        'analytic_account_id': data.get('analytic_account_id'),
                                        })]}
                            line.move_id.write(mvals)
                            updated_lines[line.id] = True
                        if updated_lines.get(line.id):
                            break
            if updated_lines:
                self.message_post(
                    body=_("%d bank statement line(s) updated.") % len(updated_lines))

    @api.model
    def match(self, bank_statement_line_pay_ref, label):
        if label in bank_statement_line_pay_ref:
            return True
        else:
            return False


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    # This is the big hack: the native method _prepare_move_line_default_vals
    # doesn't have an analytic account argument
    # So, when we want to pass an analytic account, we pass counterpart_account_id
    # as dict with 2 keys: account_id and analytic_account_id
    # This method returns [liquidity_line_vals, counterpart_line_vals]
    # => we add the analytic account in counterpart_line_vals
    @api.model
    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        counterpart_analytic_account_id = False
        if isinstance(counterpart_account_id, dict):
            counterpart_analytic_account_id = counterpart_account_id.get('analytic_account_id')
            # counterpart_account_id converted from dict to int
            counterpart_account_id = counterpart_account_id.get('account_id')
        res = super()._prepare_move_line_default_vals(counterpart_account_id=counterpart_account_id)
        if counterpart_analytic_account_id:
            return [res[0], dict(res[1], analytic_account_id=counterpart_analytic_account_id)]
        return res
