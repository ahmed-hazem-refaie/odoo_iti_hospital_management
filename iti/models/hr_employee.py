from odoo import models, fields, api


class HrEmployeeInherit(models.Model):
    # _name = "hr.employee.new"
    _inherit = "hr.employee"

    national_id = fields.Char()
