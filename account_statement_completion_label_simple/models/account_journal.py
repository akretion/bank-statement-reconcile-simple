# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models
from unidecode import unidecode
MEANINGFUL_PARTNER_NAME_MIN_SIZE = 3


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

    # automate_entry = fields.Boolean(
    #    string="Automate Entries Creation",
    #    help="Create account entries after bank statement completion "
    #         "if an account is filled on the statement line")

    def get_all_labels(self):
        self.ensure_one()
        dataset = []
        if self.statement_label_autocompletion:
            labels = self.env['account.statement.label'].search_read(
                [], ['partner_id', 'label', 'account_id'])
            for label in labels:
                dataset.append((
                    label['label'].strip().upper(),
                    label['partner_id'] and label['partner_id'][0] or False,
                    label['account_id'] and label['account_id'][0] or False))
        if self.partner_autocompletion:
            partners = self.env['res.partner'].search_read(
                [('parent_id', '=', False)], ['name'])
            for partner in partners:
                partner_name = unidecode(partner['name'].strip().upper())
                if len(partner_name) >= MEANINGFUL_PARTNER_NAME_MIN_SIZE:
                    dataset.append((partner_name, partner['id'], False))
        if self.invoice_number_autocompletion:
            invoices = self.env['account.move'].search_read([
                ('move_type', 'in', ('out_invoice', 'out_refund')),
                ('state', '=', 'posted'),
                ('company_id', '=', self.env.company.id),
                ('commercial_partner_id', '!=', False),
                ('name', '!=', False)],
                ['commercial_partner_id', 'name'])
            for invoice in invoices:
                dataset.append((
                    invoice['name'].upper(),
                    invoice['commercial_partner_id'][0],
                    False))
        # from pprint import pprint
        # pprint(dataset)
        return dataset
