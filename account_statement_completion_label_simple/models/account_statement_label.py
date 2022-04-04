# Copyright 2013-2020 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Account Statement Label"

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)],
        require=True)
    label = fields.Char('Bank Statement Label', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [(
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists in this company !'
        )]
