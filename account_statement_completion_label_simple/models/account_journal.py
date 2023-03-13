# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, _
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

#    automate_entry = fields.Boolean(
#        string="Automate Counterpart",
#        default=True,
#        help="If enabled, pre-recorded bank statement labels "
#        "configured with a counter-part account will be used to automatically set "
#        "the counter-part journal item and validate the bank statement line.")

    def get_all_labels(self):
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
                dataset.append({
                    "label": unidecode(label['label'].strip().upper()),
                    "partner_id": label['partner_id'] and label['partner_id'][0] or False,
                    "account_id": label['counterpart_account_id'] and
                    label['counterpart_account_id'][0] or False,
                })

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
                    dataset.append({
                        "label": partner_name,
                        "partner_id": partner['id'],
                    })

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
                dataset.append({
                    "label": invoice['name'].upper(),
                    "partner_id": invoice['commercial_partner_id'][0],
                })

    def _statement_line_import_speeddict(self):
        speeddict = super()._statement_line_import_speeddict()
        speeddict['labels'] = self.get_all_labels()
        return speeddict

    def _get_update_statement_line_vals_from_labels(self, stlabel, st_line_vals):
        if stlabel.get("partner_id"):
            st_line_vals['partner_id'] = stlabel["partner_id"]
        if stlabel.get("account_id"):
            st_line_vals['counterpart_account_id'] = stlabel["account_id"]
        return st_line_vals

    def _statement_line_import_update_hook(self, st_line_vals, speeddict):
        '''Match the partner from the account.statement.label'''
        super()._statement_line_import_update_hook(st_line_vals, speeddict)
        if (
                speeddict['labels'] and
                not st_line_vals.get('partner_id') and
                not st_line_vals.get('counterpart_account_id')):
            line_pay_ref = unidecode(st_line_vals['payment_ref'].upper())
            for stlabel in speeddict['labels']:
                if self.match(line_pay_ref, stlabel["label"]):
                    st_line_vals = self._get_update_statement_line_vals_from_labels(
                        stlabel, st_line_vals)
                    break

    def update_statement_lines(self):
        """Method called by the run() of the wizard account.statement.label.create"""
        self.ensure_one()
        dataset = self.get_all_labels()
        if dataset:
            lines = self.env['account.bank.statement.line'].search([
                ('journal_id', '=', self.id),
                ('partner_id', '=', False),
                ('is_reconciled', '=', False),
                ])
            updated_lines = {}
            for line in lines:
                line_pay_ref = line.payment_ref.upper()
                for stlabel in dataset:
                    if self.match(line_pay_ref, stlabel["label"]):
                        if stlabel.get("partner_id") and not line.partner_id:
                            lvals = {'partner_id': stlabel["partner_id"]}
                            line.write(lvals)
                            updated_lines[line.id] = True
                        if updated_lines.get(line.id):
                            line.move_id.message_post(body=_(
                                "Updated to partner "
                                "<a href=# data-oe-model=res.partner data-oe-id=%d>%s</a> via a new bank statement label.") % (line.partner_id.id, line.partner_id.display_name))
                            break
                        # Account is set at line creation. In case of creation of
                        # bank statement label after the statement line creation
                        # it has to be manually reconciled for now, to avoid
                        # adding too much complexity to (very) small user gain.
#                        if stlabel[2]:
#                            line.move_id.line_ids.with_context(
#                                force_delete=True).unlink()
#                            mvals = {'line_ids': [
#                                (0, 0, x) for x
#                                in line._prepare_move_line_default_vals(
#                                    counterpart_account_id=stlabel[2])]}
#                            line.move_id.write(mvals)
#                            updated_lines[line.id] = True

    @api.model
    def match(self, bank_statement_line_pay_ref, label):
        if label in bank_statement_line_pay_ref:
            return True
        else:
            return False
