Bank Statement Completion from Label (simple)
=============================================

This module provides a small and simple solution to automatically set the Partner on bank statement lines upon import of bank statement files. It also allows to automatically set a counterpart account, which can be useful for some specific statement lines.

This module is designed to be simple, both for the user and the developer!

Roadmap
=======

Usability around the "learn label" on the reconciliation widget view.
For now, when updating a partner from the learn label button, it does not update refresh the parner on the left screen (on the statement line kanban)
Also, on the reconcile tab, the partner is not set by default as the filter.

When learning a label with an account, it is not updated on the reconciliation widget, the user still has to reconcile the line manually.
It will be taken into account on next statement line creation matching this new label.
Automatically reconcile from learn label button in case of counter part account seems to add a lot of complexity for a small gain, but it would be doable.

Credits
=======

Authors
~~~~~~~

* Akretion

Contributors
~~~~~~~~~~~~

* Alexis de Lattre <alexis.delattre@akretion.com>
* Florian da Costa
