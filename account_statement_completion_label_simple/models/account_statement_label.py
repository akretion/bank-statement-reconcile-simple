# Copyright 2013-2022 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Account Statement Label"

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)])
    account_id = fields.Many2one(
        'account.account', 'Account',
        help="It will automatically create a accounting entry for the "
             "statement line and won't propose the reconciliation")
    label = fields.Char('Bank Statement Label', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [(
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists in this company !'
        )]

    @api.constrains('partner_id', 'account_id')
    def label_check(self):
        for label in self:
            if not label.partner_id and not label.account_id:
                raise ValidationError(_(
                    "The bank statement label '%s' should have either "
                    "a partner or an account.") % label.label)
