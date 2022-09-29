# Copyright 2015-2022 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Completion from Label (simple)',
    'version': '14.0.2.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
This module provides a small and simple solution to automatically set the Partner on bank statement lines upon import of bank statement files. It also allows to automatically set a counterpart account, which can be useful for some specific statement lines.

This module is designed to be simple, both for the user and the developer!

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/bank-statement-reconcile-simple',
    'depends': [
        'account_statement_import_base',
        'account_menu',
        ],
    'external_dependencies': {'python': ['unidecode']},
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'wizard/account_statement_label_create_view.xml',
        'wizard/res_config_settings_views.xml',
        'views/account_bank_statement.xml',
        'views/account_statement_label.xml',
        'views/res_partner.xml',
        'views/account_journal.xml',
    ],
    'installable': True,
}
