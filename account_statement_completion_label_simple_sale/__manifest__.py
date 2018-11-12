# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Completion from Label - Sale extension',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'description': """
This module is a small auto-install module for Odoo installations that used both the *sale_commercial_partner* and *account_statement_completion_label_simple* modules.

See the description of the module *account_statement_completion_label_simple* for more information.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account_statement_completion_label_simple', 'sale_commercial_partner'],
    'data': [
        'views/account_journal.xml',
    ],
    'installable': True,
    'auto_install': True,
}
