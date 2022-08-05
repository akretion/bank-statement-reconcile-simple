# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    statement_autocompletion_partner_name_min_size = fields.Integer(
        related="company_id.statement_autocompletion_partner_name_min_size",
        readonly=False)
