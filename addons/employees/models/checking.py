# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api,  _
import calendar
from odoo.exceptions import ValidationError
from datetime import datetime, date

class EmployeeTimesheet(models.Model):
    _name = 'employees.checking'
    _description = 'Chấm công'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date"
    
    @api.onchange('date')
    def _get_day_of_date(self):

        for r in self:
            if r.date :
                selected = fields.Datetime.from_string(r.date)
                r.date_day = calendar.day_name[selected.weekday()]
                if r.date_day == "Monday":
                    r.date_day = "Thứ 2"
                if r.date_day == "Tuesday":
                    r.date_day = "Thứ 3"
                if r.date_day == "Wednesday":
                    r.date_day = "Thứ 4"
                if r.date_day == "Thursday":
                    r.date_day = "Thứ 5"
                if r.date_day == "Friday":
                    r.date_day = "Thứ 6"
                if r.date_day == "Saturday":
                    r.date_day = "Thứ 7"
                if r.date_day == "Sunday":
                    r.date_day = "Chủ nhật" 
            else:
                r.date_day = ""
                

    employee_id  = fields.Many2one('employees.employee', string='Mã nhân sự', required=True)
    time_checking = fields.Float(string='Giờ checking')
    date = fields.Date(string='Ngày')
    date_day = fields.Char('Thứ', compute='_get_day_of_date')
    device_id = fields.Integer('device_id') 
    notes = fields.Text(string='Ghi chú')
    user_has_scheduler = fields.Many2one('employees.user.has.scheduler', string="Bảng chấm công")
    total_late = fields.Integer('Tổng số phút đi muộn') 
    method_work = fields.Selection('Phương thức làm việc', related='employee_id.method_work')
    status_work = fields.Selection('Mã chấm công', related='employee_id.status_work')
    department_id = fields.Many2one('employees.department', string='Phòng/ban',  related='employee_id.department_id')
    total  = fields.Float(string='Tổng công')

