# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountStatementLabel(models.Model):
    _inherit = "account.statement.label"

    account_id = fields.Many2one(
        'account.account', 'Account',
        help="It will automatically create a accounting entry for the "
             "statement line and won't propose the reconciliation")
