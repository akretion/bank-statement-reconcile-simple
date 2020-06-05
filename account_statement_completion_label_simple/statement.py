# Copyright 2013-2019 Akretion France (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# @author Alexis de LATTRE <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from unidecode import unidecode
MEANINGFUL_PARTNER_NAME_MIN_SIZE = 3


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    def create_line_entries_from_account(self):
        for stmt in self:
            st_lines = self.env['account.bank.statement.line'].search([
                ('statement_id', '=', stmt.id),
                ('account_id', '!=', False),
                ('journal_entry_ids', '=', False),
                ])
            st_lines.fast_counterpart_creation()
            if stmt.all_lines_reconciled and stmt.state == 'draft':
                stmt.button_confirm_bank()

    def update_statement_lines(self):
        self.ensure_one()
        dataset = self.get_all_labels(self.journal_id)
        if dataset:
            lines = self.env['account.bank.statement.line'].search([
                ('statement_id', '=', self.id),
                ('partner_id', '=', False),
                ('account_id', '=', False),
                ('journal_entry_ids', '=', False),
                ])
            for line in lines:
                line_name = line.name.upper()
                for stlabel in dataset:
                    if self.match(line_name, stlabel[0]):
                        lvals = {'partner_id': stlabel[1]}
                        if stlabel[2]:
                            lvals['account_id'] = stlabel[2]
                        line.write(lvals)
                        break
        if self.journal_id.automate_entry:
            self.create_line_entries_from_account()
        return True

    @api.model
    def match(self, bank_statement_line_name, label):
        if label in bank_statement_line_name:
            return True
        else:
            return False

    @api.model
    def get_all_labels(self, journal):
        dataset = []
        if journal.statement_label_autocompletion:
            labels = self.env['account.statement.label'].search_read(
                [], ['partner_id', 'label', 'account_id'])
            for label in labels:
                dataset.append((
                    label['label'].strip().upper(),
                    label['partner_id'] and label['partner_id'][0] or False,
                    label['account_id'] and label['account_id'][0] or False))
        if journal.partner_autocompletion:
            partners = self.env['res.partner'].search_read(
                [('parent_id', '=', False)], ['name'])
            for partner in partners:
                partner_name = unidecode(partner['name'].strip().upper())
                if len(partner_name) >= MEANINGFUL_PARTNER_NAME_MIN_SIZE:
                    dataset.append((partner_name, partner['id'], False))
        if journal.invoice_number_autocompletion:
            invoices = self.env['account.move'].search_read([
                ('type', 'in', ('out_invoice', 'out_refund')),
                ('state', '=', 'posted'),
                ('company_id', '=', self.env.user.company_id.id),
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


class AccountStatementLabel(models.Model):
    """Create a new class to map an account statement label to a partner"""
    _name = "account.statement.label"
    _description = "Account Statement Label"

    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='cascade',
        domain=[('parent_id', '=', False)])
    account_id = fields.Many2one(
        'account.account', 'Account',
        help="It will automatically create a accounting entry for the "
             "statement line and won't propose the reconciliation")
    label = fields.Char('Bank Statement Label', required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [(
        'label_company_unique', 'unique(label, company_id)',
        'This label already exists in this company !'
        )]

    @api.constrains('partner_id', 'account_id')
    def label_check(self):
        for label in self:
            if not label.partner_id and not label.account_id:
                raise ValidationError(_(
                    "The bank statement label '%s' should have either "
                    "a partner or an account.") % label.label)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_statement_label_ids = fields.One2many(
        'account.statement.label', 'partner_id',
        string='Bank Statement Labels')
    bank_statement_label_count = fields.Integer(
        compute='_compute_bank_statement_label_count',
        string='Number of Bank Statement Labels', readonly=True)

    def _compute_bank_statement_label_count(self):
        label_data = self.env['account.statement.label'].read_group(
            [('partner_id', 'in', self.ids)], ['partner_id'], ['partner_id'])
        mapped_data = dict([
            (label['partner_id'][0], label['partner_id_count'])
            for label in label_data])
        for partner in self:
            partner.bank_statement_label_count = mapped_data.get(partner.id, 0)
