# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_completion_label_simple for Odoo
#   Copyright (C) 2015-2016 Akretion (http://www.akretion.com)
#   @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Bank Statement Completion from Label (simple)',
    'version': '0.2',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'description': """
This module is a simple equivalent of the module *account_statement_completion_label* (from the OCA branch *bank-statement-reconcile*) for Odoo version 8. It's only dependancy is the module *account_bank_statement_import* from the OCA branch *bank-statement-import*.

These 2 modules have the same datamodel for the important fields of the object account.statement.label, so the migration from this module to the other module should be easy.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account_bank_statement_import'],
    'external_dependencies': {'python': ['unidecode']},
    'data': [
        'partner_view.xml',
        'statement_view.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'company_view.xml',
    ],
    'installable': True,
}
