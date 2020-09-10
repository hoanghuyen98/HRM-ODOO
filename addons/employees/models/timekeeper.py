# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class Timekeeper(models.Model):
    _name = "employees.timekeeper"
    _description = "Máy chấm công"

    # add new field
    name = fields.Char('Tên máy', required=True)
    type_conn = fields.Selection([
        ('tcp/ip', 'TCP/IP'),
        ('usb', 'USB'),
        ('r232/rs485', 'R232/RS485'),

    ], string='Loại kết nối', default='tcp/ip')

    port_com = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    ], string='Cổng COM', default='1')

    speed_com = fields.Selection([
        ('115200', '115200'),
        ('57600', '57600'),
        ('38400', '38400'),
        ('19200', '19200'),
        ('9600', '9600'),
    ], string='Tốc độ COM', default='115200')
    domain =  fields.Char('Tên miền')
    