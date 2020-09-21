# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class EmployeeReport(models.Model):
    _name = "employees.user.has.scheduler"
    _description = "Export báo cáo"

    def print_report(self):
        data = {
            'model': 'create.report',
            'form': self.read()[0]
        }
        
        return self.env.ref('employees.report_checking_card_xls').report_action(self)

    employee_line = fields.One2many('employee.lines','report_id_user', string='Nhân viên')
    start_date = fields.Date(string='Từ ngày')
    end_date = fields.Date(string='Đến ngày')
    scheduler_id = fields.Many2one('employees.scheduler', string='Ca làm việc')
    note = fields.Text('Ghi chú', default="s")

class EmployeeReportLines(models.Model):
    _name = 'employee.lines'
    _description = 'Appointment Lines'

    employee_name = fields.Many2one('employees.employee', string='Nhân viên')
    type_report = fields.Selection([
        ('all', 'Tất cả nhân viên'),
        ('clone', 'Từng nhân viên'),
    ], string='Phương thức', default='all')
    product_qty = fields.Integer(string="Quantity")
    report_id_user = fields.Many2one('employees.user.has.scheduler', string='Report ID')
    method_work = fields.Selection('Phương thức làm việc', related='employee_name.method_work')
    status_work = fields.Selection('Mã chấm công', related='employee_name.status_work')
    department_id = fields.Many2one('employees.department', string='Phòng/ban',  related='employee_name.department_id')
    # display_type = fields.Selection([
    #     ('line_section', "Section"),
    #     ('line_note', "Note")], default=False, help="Technical field for UX purpose.")