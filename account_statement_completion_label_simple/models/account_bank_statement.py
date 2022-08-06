# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# @author: Florian da Costa <florian.dacosta@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


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
            for line in lines:
                line_pay_ref = line.payment_ref.upper()
                for stlabel in dataset:
                    if self.match(line_pay_ref, stlabel[0]):
                        if stlabel[1] and not line.partner_id:
                            lvals = {'partner_id': stlabel[1]}
                            line.write(lvals)
                        if stlabel[2]:
                            line.move_id.line_ids.with_context(
                                force_delete=True).unlink()
                            mvals = {'line_ids': [
                                (0, 0, x) for x
                                in line._prepare_move_line_default_vals(
                                    counterpart_account_id=stlabel[2])]}
                            line.move_id.write(mvals)
                        break

    @api.model
    def match(self, bank_statement_line_pay_ref, label):
        if label in bank_statement_line_pay_ref:
            return True
        else:
            return False
