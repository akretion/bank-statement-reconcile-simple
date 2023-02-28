# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# @author: Florian da Costa <florian.dacosta@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def update_statement_lines(self):
        """Method called by the button on bank statement form view"""
        journal = self.journal_id
        if len(journal) != 1:
            raise # TODO
        dataset = journal.get_all_labels()
        if dataset:
            lines = self.env['account.bank.statement.line'].search([
                ('id', 'in', self.ids),
                ('is_reconciled', '=', False),
                ])
            updated_lines = {}
            for line in lines:
                line_pay_ref = line.payment_ref.upper()
                for stlabel in dataset:
                    if self.match(line_pay_ref, stlabel["label"]):
                        if stlabel.get("partner_id") and not line.partner_id:
                            lvals = {'partner_id': stlabel["partner_id"]}
                            line.write(lvals)
                            updated_lines[line.id] = True
                        if updated_lines.get(line.id):
                            line.move_id.message_post(
                                body=_("bank statement line updated with partner %s") % line.partner_id.name)
                            break
                        # Account is set at line creation. In case of creation of 
                        # bank statement label after the statement line creation
                        # it has to be manually reconciled for now, to avoid
                        # adding too much complexity to (very) small user gain.
#                        if stlabel[2]:
#                            line.move_id.line_ids.with_context(
#                                force_delete=True).unlink()
#                            mvals = {'line_ids': [
#                                (0, 0, x) for x
#                                in line._prepare_move_line_default_vals(
#                                    counterpart_account_id=stlabel[2])]}
#                            line.move_id.write(mvals)
#                            updated_lines[line.id] = True

    @api.model
    def match(self, bank_statement_line_pay_ref, label):
        if label in bank_statement_line_pay_ref:
            return True
        else:
            return False
