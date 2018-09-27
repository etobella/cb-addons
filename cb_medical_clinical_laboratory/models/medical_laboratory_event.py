# Copyright 2017 Creu Blanca
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MedicalLaboratoryEvent(models.Model):
    _inherit = 'medical.laboratory.event'

    delay = fields.Integer(
        help='Number of days until it will be finished'
    )
    cost = fields.Monetary(required=True, default=0)
