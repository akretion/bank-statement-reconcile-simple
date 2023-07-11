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
                for stlabel in dataset:
                    if self.match(line_pay_ref, stlabel[0]):
                        line._update_line_from_label(stlabel, updated_lines)
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

    def _update_line_from_label(self, label, updated_lines):
        self.ensure_one()
        if label[1] and not self.partner_id:
            lvals = {'partner_id': label[1]}
            self.write(lvals)
            updated_lines[self.id] = True
        if label[2]:
            self._update_counterpart_account(label[2])
            updated_lines[self.id] = True

    def _update_counterpart_account(self, account_id):
        self.ensure_one()
        self.move_id.line_ids.with_context(
        force_delete=True).unlink()
        mvals = {'line_ids': [
            (0, 0, x) for x
            in self._prepare_move_line_default_vals(
                counterpart_account_id=account_id)]}
        self.move_id.write(mvals)
