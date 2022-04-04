# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def _get_dataset_from_label(self, label):
        dataset = super()._get_dataset_from_label(label)
        dataset = dataset + (label['account_id'] and label['account_id'][0] or False,)
        return dataset

    def _get_label_fields(self):
        fields = super()._get_label_fields()
        return fields.append("account_id")
