# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion France (http://www.akretion.com/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    statement_label_autocompletion = fields.Boolean(
        string="Label Completion",
        default=True,
        help="If enabled, the partner field of bank statement lines "
        "will be automatically set if it contains the label "
        "of a bank statement label.")

    partner_autocompletion = fields.Boolean(
        string="Partner Completion",
        default=True,
        help="If enabled, the partner field of bank statement lines "
        "will be automatically set if it contains the exact "
        "name of a partner.")

    invoice_number_autocompletion = fields.Boolean(
        string="Invoice Number Completion",
        default=True,
        help="If enabled, the partner field of bank statement "
        "lines will be automatically set if it contains a customer "
        "invoice/refund number.")

    automate_entry = fields.Boolean(
        string="Automate Entries Creation",
        help="Create account entries after bank statement completion "
             "if an account is filled on the statement line")
