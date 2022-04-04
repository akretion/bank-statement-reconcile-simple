# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountStatementLabelCreate(models.TransientModel):
    _inherit = 'account.statement.label.create'

    account_id = fields.Many2one('account.account')
