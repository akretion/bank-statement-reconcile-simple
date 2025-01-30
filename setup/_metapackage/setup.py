import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-akretion-bank-statement-reconcile-simple",
    description="Meta package for akretion-bank-statement-reconcile-simple Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-account_statement_completion_label_simple',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
