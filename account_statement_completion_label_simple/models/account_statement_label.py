# Copyright 2013-2020 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Account Statement Label"
    _check_company_auto = True

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)], check_company=True)
    counterpart_account_id = fields.Many2one(  # TODO rename field too ?
        'account.account', 'Counterpart Account',
        help="When you start processing the bank statement, "
        "It will automatically process the statement line "
        "with that account as counterpart.")
    counterpart_type = fields.Selection([
        ('auto', 'Automatic'),
        ('suggest', 'Suggest'),
        ], string='Processing Type')
    label = fields.Char('Bank Statement Label', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [(
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists in this company !'
        )]

    @api.constrains('partner_id', 'counterpart_account_id')
    def label_check(self):
        for label in self:
            if not label.partner_id and not label.counterpart_account_id:
                raise ValidationError(_(
                    "The bank statement label '%s' should have either "
                    "a partner or a counterpart account.") % label.label)
