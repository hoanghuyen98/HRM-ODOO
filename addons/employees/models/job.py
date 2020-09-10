# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class EmployeeJob(models.Model):
    _name = "employees.job"
    _description = "Employee Job"

    # add new field
    name = fields.Char('Chức vụ', required=True)
    employee_id = fields.One2many('employees.employee', 'department_id',string='Nhân viên')
    # department_id = fields.Many2one('employee.department',string='Phòng/ban', required=True)
    department_id = fields.Many2one('employees.department', string='Phòng/ban',  related='employee_id.department_id')
    note = fields.Text('Ghi chú')
    # company_id = fields.Many2one(string='Công ty')
