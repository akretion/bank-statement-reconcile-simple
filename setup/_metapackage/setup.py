import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-akretion-bank-statement-reconcile-simple",
    description="Meta package for akretion-bank-statement-reconcile-simple Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-account_statement_completion_label_simple>=15.0dev,<15.1dev',
        'odoo-addon-account_statement_completion_label_simple_sale>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
