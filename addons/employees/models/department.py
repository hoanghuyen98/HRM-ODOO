# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Department(models.Model):
    _name = "employees.department"
    _description = "Employee Department"
    # add new field
    name = fields.Char(string='Tên phòng/ban', required=True)
    parent_id = fields.Many2one('employees.department', string='Phòng/Ban cấp trên')
    manager_id = fields.Many2one('employees.employee', string='Người quản lý')
    note = fields.Text('Ghi chú')
