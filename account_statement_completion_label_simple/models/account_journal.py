# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models
from unidecode import unidecode


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    statement_label_autocompletion = fields.Boolean(
        string="Label Completion",
        default=True,
        help="If enabled, the partner field of bank statement lines "
        "will be automatically set if it contains the label "
        "of a bank statement label with a partner.")

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
        string="Automate Counterpart",
        default=True,
        help="If enabled, a specific counterpart account will be "
        "automatically set and the statement line will be auto-validated "
        "if it contains the label of a bank statement label with a counterpart "
        "account.")

    def get_all_labels(self):
        # TODO cut this method for easier inheritance
        self.ensure_one()
        dataset = []
        self._statement_label_get_all_labels(dataset)
        self._partner_get_all_labels(dataset)
        self._invoice_get_all_labels(dataset)
        # from pprint import pprint
        # pprint(dataset)
        return dataset

    def _statement_label_get_all_labels(self, dataset):
        if self.statement_label_autocompletion:
            labels = self.env['account.statement.label'].search_read(
                [
                    '|',
                    ('company_id', '=', False),
                    ('company_id', '=', self.company_id.id),
                ],
                ['partner_id', 'label', 'counterpart_account_id'])
            for label in labels:
                dataset.append((
                    label['label'].strip().upper(),
                    label['partner_id'] and label['partner_id'][0] or False,
                    label['counterpart_account_id'] and
                    label['counterpart_account_id'][0] or False))

    def _partner_get_all_labels(self, dataset):
        if self.partner_autocompletion:
            partner_name_min_size =\
                self.company_id.statement_autocompletion_partner_name_min_size
            partners = self.env['res.partner'].search_read(
                [
                    '|',
                    ('company_id', '=', False),
                    ('company_id', '=', self.company_id.id),
                    ('parent_id', '=', False),
                ],
                ['name'])
            for partner in partners:
                partner_name = unidecode(partner['name'].strip().upper())
                if len(partner_name) >= partner_name_min_size:
                    dataset.append((partner_name, partner['id'], False))

    def _invoice_get_all_labels(self, dataset):
        if self.invoice_number_autocompletion:
            invoices = self.env['account.move'].search_read([
                ('move_type', 'in', ('out_invoice', 'out_refund')),
                ('state', '=', 'posted'),
                ('company_id', '=', self.company_id.id),
                ('commercial_partner_id', '!=', False),
                ('name', '!=', False)],
                ['commercial_partner_id', 'name'])
            for invoice in invoices:
                dataset.append((
                    invoice['name'].upper(),
                    invoice['commercial_partner_id'][0],
                    False))
