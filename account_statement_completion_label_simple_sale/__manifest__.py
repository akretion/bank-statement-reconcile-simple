# Copyright 2018-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Completion from Label - Sale extension',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/bank-statement-reconcile-simple',
    'depends': ['account_statement_completion_label_simple', 'sale_commercial_partner'],
    'data': [
        'views/account_journal.xml',
    ],
    'installable': True,
    'auto_install': True,
}
