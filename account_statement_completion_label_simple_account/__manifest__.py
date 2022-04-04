# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Completion from Label (Account)',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': """
        Extend account_statement_completion_label_simple to add the account on the
        bank statement line. If it is the case, the reconciliation process for the
        line will be bypassed, the counterpart will automatically be on the found
        account.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['account_statement_completion_label_simple', "account_reconciliation_widget"],
    'data': [
        'wizard/account_statement_label_create_view.xml',
        'views/account_bank_statement.xml',
        'views/account_statement_label.xml',
    ],
    'installable': True,
}
