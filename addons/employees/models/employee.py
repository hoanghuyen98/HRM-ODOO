# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Employee(models.Model):
    _name = "employees.employee"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Table"

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id, '%s - %s - %s' % (rec.id, rec.name, rec.name_seq)))
        return res

    name = fields.Char(string='Mã nhân sự', required=True)
    name_seq = fields.Char(string='Tên nhân sự', required=False, )
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')
    method_work = fields.Selection([
        ('fulltime', 'Fulltime'),
        ('parttime', 'Parttime')
    ], string='Phương thức làm việc', default='fulltime')
    timesheet_id = fields.Char('Mã chấm công', required=False)
    x_wage = fields.Integer('Mức lương', default=0) 
    status_work = fields.Selection([
        ('inactive', 'Đã nghỉ làm'),
        ('active', 'Đang làm việc'),
    ], string='Trạng thái', default='active')
    image = fields.Binary(string='Image', attachment=True)
    department_id = fields.Many2one('employees.department', string="Đơn vị")
    job_id = fields.Many2one('employees.job', string="Chức vụ")
