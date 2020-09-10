# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class EmployeeComeHomeEarly(models.Model):
    _name = "employees.setting"
    _description = "Cài đặt"

    # add new field
    # name = fields.Char('Chức vụ', required=True)
    # employee_id = fields.One2many('employees.employee', 'department_id',string='Nhân viên')
    # # department_id = fields.Many2one('employee.department',string='Phòng/ban', required=True)
    # department_id = fields.Many2one('employees.department', string='Phòng/ban',  related='employee_id.department_id')
    # note = fields.Text('Ghi chú')
    # company_id = fields.Many2one(string='Công ty')
    # member_ids= fields.One2many('employee',string='Thành viên')
    # modify old fields
    # gender = fields.Selection(selection_add=[('sterilization', 'Sterilization')]) 