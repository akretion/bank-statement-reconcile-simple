import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-akretion-bank-statement-reconcile-simple",
    description="Meta package for akretion-bank-statement-reconcile-simple Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-account_statement_completion_label_simple',
        'odoo14-addon-account_statement_completion_label_simple_sale',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
