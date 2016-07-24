# -*- coding: utf-8 -*-
###############################################################################
#
#   account_statement_completion_label_simple for Odoo
#   Copyright (C) 2013-2016 Akretion (http://www.akretion.com)
#   @author Florian DA COSTA <florian.dacosta@akretion.com>
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

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_complete_from_partner_name = fields.Boolean()
