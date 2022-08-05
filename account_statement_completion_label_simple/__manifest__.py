# Copyright 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Completion from Label (simple)',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
This module is a simple equivalent of the module *account_statement_completion_label* (from the OCA project *bank-statement-reconcile*). It's only dependancy is the module *account_bank_statement_import* from the official addons.

These 2 modules have the same datamodel for the important fields of the object account.statement.label, so the migration from this module to the other module should be easy.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account_statement_import'],
    'external_dependencies': {'python': ['unidecode']},
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'wizard/account_statement_label_create_view.xml',
        'wizard/res_config_settings_views.xml',
        'views/account_bank_statement.xml',
        'views/account_statement_label.xml',
        'views/partner.xml',
        'views/account_journal.xml',
    ],
    'installable': True,
}
