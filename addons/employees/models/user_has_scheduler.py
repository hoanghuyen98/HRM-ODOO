# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class EmployeeJob(models.Model):
    _name = "employees.user.has.scheduler"
    _description = "Employee User has scheduler"


    employee_id = fields.Many2one('employees.employee', string='Nhân viên', required=True)
    # department_id = fields.Many2one('employee.department',string='Phòng/ban', required=True)
    scheduler_id = fields.Many2one('employees.scheduler', string='Ca làm việc')
    # checking_id = fields.One2many('employees.checking', string='Chấm công')
    note = fields.Text('Ghi chú')