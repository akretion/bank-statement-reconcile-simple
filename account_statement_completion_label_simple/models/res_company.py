# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    statement_autocompletion_partner_name_min_size = fields.Integer(
        string='Partner Name Min Size', default=4)

    _sql_constraints = [(
        'statement_autocompletion_partner_name_min_size_constraint',
        'CHECK(statement_autocompletion_partner_name_min_size >= 1)',
        'The minimum value for Partner Name Min Size is 1.',
        )]
