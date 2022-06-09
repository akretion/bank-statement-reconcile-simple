# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountStatementLabelCreate(models.TransientModel):
    _inherit = 'account.statement.label.create'

    account_id = fields.Many2one('account.account')

    def _get_label_vals(self):
        vals = super()._get_label_vals()
        if self.account_id:
            vals["account_id"] = self.account_id.id
        return vals
