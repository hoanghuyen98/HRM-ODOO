# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class EmployeeScheduler(models.Model):
    _name = "employees.scheduler"
    _description = "Employee scheduler"
    _rec_name = 'shift_id'

    @api.constrains('time_start', 'time_finish', 'timesleep_start', 'timesleep_finish')
    def get_total_hours(self):
        for rec in self:
            if (rec.time_finish >= rec.time_start):
                if (rec.timesleep_finish >= rec.timesleep_start):
                    rec.total_hours = (rec.time_finish - rec.time_start)*60 - (rec.timesleep_finish-rec.timesleep_start)*60
                else:
                    raise ValidationError(_('Giờ kết thúc nghỉ trưa phải lớn hơn giờ bắt đầu nghỉ trưa !'))
            else:
                raise ValidationError(_('Giờ kết thúc làm việc phải lớn hơn giờ bắt đầu làm việc !'))

    
    shift_id = fields.Char('Mã ca làm việc', required=True)
    time_start = fields.Float(string='Giờ bắt đầu ca làm việc')
    time_finish = fields.Float(string='Giờ kết thúc ca làm việc')
    timesleep_start = fields.Float(string='Giờ bắt đầu nghỉ trưa')
    timesleep_finish = fields.Float(string='Giờ kết thúc nghỉ trưa')
    count_the_work = fields.Float('Số công')
    total_hours = fields.Integer('Tổng số phút', compute='get_total_hours')
