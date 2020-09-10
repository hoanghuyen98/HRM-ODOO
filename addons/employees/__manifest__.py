# -*- coding: utf-8 -*-
{
    'name': "Nhân sự",
    'version': '13.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """nhân sự""",
    'description': """Quản lý nhân sự""",
    'author': "admin",
    'website': "odoo.com",
    'license': 'AGPL-3',
    'depends': ['mail', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee.xml',
        'views/department.xml',
        'views/job.xml',
        'views/checking.xml',
        'views/templates.xml',
        'views/scheduler.xml',
        'views/user_has_scheduler.xml',
        'views/timekeeper.xml',
        'reports/report.xml',
        'reports/checking_card.xml',

    ],
    'images': ['static/description/banner.png'],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    # 'auto_install': False
}