# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Bank Statement Label"
    _rec_name = "label"
    _check_company_auto = True

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)], check_company=True)
    counterpart_account_id = fields.Many2one(
        'account.account', string='Counterpart Account', check_company=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]",
        help="When you import the bank statement, "
        "it will automatically process the matched statement line "
        "with that account as counterpart.")
    label = fields.Char('Bank Statement Label', required=True)
    # WARNING: company_id is NOT required=True
    # it is only required when counterpart_account_id is set
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [(
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists!'
        )]

    @api.constrains('partner_id', 'counterpart_account_id', 'company_id')
    def _label_check(self):
        for label in self:
            if not label.partner_id and not label.counterpart_account_id:
                raise ValidationError(_(
                    "The bank statement label '%s' should have either "
                    "a partner or a counterpart account.") % label.label)
            if label.counterpart_account_id and not label.company_id:
                raise ValidationError(_(
                    "The bank statement label '%s' has a Counterpart "
                    "Account, so it must be linked to a Company "
                    "(the company of the Counterpart Account).")
                    % label.label)
