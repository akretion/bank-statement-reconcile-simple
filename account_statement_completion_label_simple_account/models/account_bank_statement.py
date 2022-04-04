# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def _get_vals_from_stlabel(self, stlabel):
        vals = super()._get_vals_from_stlabel(stlabel)
        if len(stlabel) > 2 and stlabel[2]:
            vals["account_id"] = stlabel[2]
        return vals

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

    # Note it does not seem usefull to override _synchronize_from_moves :
    # indeed, the move's account_id can't be modified if move is posted and the
    # move can't go back to draft if st line is validated. So for the move account_id to
    # change, statement needs to go back to draft which reset all amt to suspend account
    # anyway
    # _synchronize_to_moves does not seem usefull for the same reason, statement line
    # can only change when statement is draft...the in case of change, it will be
    # be propataged to the move during the statement posting
