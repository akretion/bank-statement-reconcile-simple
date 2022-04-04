# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountStatementImport(models.TransientModel):
    _inherit = 'account.statement.import'

    def _complete_vals_from_label(self, vals, stlabel):
        vals = super()._complete_vals_from_label(vals, stlabel)
        if len(stlabel) > 2:
            vals["account_id"] = stlabel[2]
        return vals
