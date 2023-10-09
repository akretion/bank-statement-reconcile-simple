# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models
from unidecode import unidecode


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    statement_label_autocompletion = fields.Boolean(
        string="Label Completion",
        default=True,
        help="If enabled, pre-recorded bank statement labels "
        "configured with a partner will be used to automatically set "
        "the partner on bank statement lines.")

    partner_autocompletion = fields.Boolean(
        string="Partner Name Completion",
        help="If enabled, the partner will be set automatically on a "
        "bank statement line if it contains the exact name of that partner "
        "(independenly of accents and letter case).")

    invoice_number_autocompletion = fields.Boolean(
        string="Invoice Number Completion",
        default=True,
        help="If enabled, the partner will be set automatically on a "
        "bank statement line if it contains a customer invoice/refund number "
        "of that partner.")

    automate_entry = fields.Boolean(
        string="Automate Counterpart",
        default=True,
        help="If enabled, pre-recorded bank statement labels "
        "configured with a counter-part account will be used to automatically set "
        "the counter-part journal item and validate the bank statement line.")

    def get_all_labels(self):
        self.ensure_one()
        dataset = {}
        self._statement_label_get_all_labels(dataset)
        self._partner_get_all_labels(dataset)
        self._invoice_get_all_labels(dataset)
        # from pprint import pprint
        # pprint(dataset)
        return dataset

    def _statement_label_get_all_labels(self, dataset):
        if self.statement_label_autocompletion:
            entries = self.env['account.statement.label'].search_read(
                [
                    '|',
                    ('company_id', '=', False),
                    ('company_id', '=', self.company_id.id),
                ],
                [
                    'partner_id',
                    'label',
                    'counterpart_account_id',
                    'counterpart_analytic_account_id',
                    ])
            for entry in entries:
                label = unidecode(entry['label'].strip().upper())
                vals = {}
                if entry['partner_id']:
                    vals['partner_id'] = entry['partner_id'][0]
                if entry['counterpart_account_id']:
                    vals['account_id'] = entry['counterpart_account_id'][0]
                    vals['analytic_account_id'] = entry['counterpart_analytic_account_id'] and entry['counterpart_analytic_account_id'][0] or False
                dataset[label] = vals

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
                    dataset[partner_name] = {'partner_id': partner['id']}

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
                dataset[invoice['name'].upper()] = {
                    'partner_id': invoice['commercial_partner_id'][0],
                    }

    def _statement_line_import_speeddict(self):
        speeddict = super()._statement_line_import_speeddict()
        speeddict['labels'] = self.get_all_labels()
        return speeddict

    def _statement_line_import_update_hook(self, st_line_vals, speeddict):
        '''Match the partner from the account.statement.label'''
        super()._statement_line_import_update_hook(st_line_vals, speeddict)
        abso = self.env['account.bank.statement']
        if (
                speeddict['labels'] and
                not st_line_vals.get('partner_id') and
                not st_line_vals.get('counterpart_account_id')):
            line_pay_ref = unidecode(st_line_vals['payment_ref'].upper())
            for label, data in speeddict['labels'].items():
                if abso.match(line_pay_ref, label):
                    if data.get('partner_id'):
                        st_line_vals['partner_id'] = data['partner_id']
                    if data.get('account_id'):
                        st_line_vals['counterpart_account_id'] = {
                            'account_id': data['account_id'],
                            'analytic_account_id': data.get('analytic_account_id'),
                            }
                    break
