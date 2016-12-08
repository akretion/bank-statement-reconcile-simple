# -*- coding: utf-8 -*-
# © 2016 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = 'account.journal'

    statement_label_autocompletion = fields.Boolean(
        string="Label Completion",
        default=True,
        help="If ticked, after import the bank statement will be "
             "auto-completed based on bank statement labels")

    partner_autocompletion = fields.Boolean(
        string="Partner Completion",
        default=True,
        help="If ticked, after import the bank statement will be "
             "auto-completed based on all partner's names")

    automate_entry = fields.Boolean(
        string="Automate entries creation",
        help="Create account entries after bank statement completion "
             "if an account is filled on the statement line")
