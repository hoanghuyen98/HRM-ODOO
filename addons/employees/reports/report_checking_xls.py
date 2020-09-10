from odoo import models
import calendar
import pytz
from . import Const
from odoo import models, fields, api,  _
from datetime import datetime, date
class CheckingALLXlsx(models.AbstractModel):
    _name = 'report.employees.report_checking_xls'
    _inherit = 'report.report_xlsx.abstract'
    
         
    def get_lines(self, data):
        lines = []
        employee_id = data.employee_id.mapped('id')
        if employee_id:
            employee = self.env['employees.checking'].search([('employee_id', 'in', employee_id)])

        else:
            employee = self.env['employees.checking'].search([])
        # product_ids = tuple([pro_id.id for pro_id in categ_products])
        employee_query = """
            SELECT date, employee_id, max(time_checking), min(time_checking) FROM employees_checking 
            
            GROUP BY date, employee_id 
            ORDER BY  date
            """
        params = employee_id if employee_id else (0, 0)
        self._cr.execute(employee_query, params)
        sol_query_obj = self._cr.dictfetchall()

        list_employee_repory = []
        records = 0
        for item in sol_query_obj:
            check_in = 0
            check_out = 0
    
            for obj in employee:
                if int(item['employee_id']) == obj.employee_id.id:
                    seen = set()
                    new_l = []
                   
                    vals = {
                        'id': obj.employee_id.name,
                        'employee_id': obj.employee_id.name_seq,
                        'date': item['date'],
                        'department': obj.employee_id.department_id.name,
                        'method_work': obj.employee_id.method_work,
                        # 'day': obj.,
                        # 'available': str(sol_query_obj),
                        'check_in': item['min'],
                        'check_out': item['max'],
                        # 'date': obj.date,
                        # 'obj': obj,
                        # # 'total_value': value,
                        # # 'sale_value': sale_value,
                        # # 'purchase_value': purchase_value,
                    }
            
            
                    lines.append(vals)
                    break
            
        return lines

    def generate_xlsx_report(self, workbook, data, lines):
        # for obj in lines: 
        sheet = workbook.add_worksheet('Chấm công')
        # date = monthrange(year, month)
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        # sheet.merge_range(1, 0, 4, 0, 'Mã NV', format21)
        sheet.merge_range(4, 0, 2, 2, 'Họ tên', format21)
        sheet.merge_range(4, 3, 2, 4, 'Team', format21)
        sheet.merge_range(4, 5, 2, 6, 'Trạng thái', format21)
        sheet.merge_range(4, 7, 2, 8, 'Ngày', format21)
        sheet.merge_range(4, 9, 2, 10, 'Thứ', format21)
        sheet.merge_range(4, 11, 2, 12, 'Giờ đến', format21)
        sheet.merge_range(4, 13, 2, 14, 'Giờ về', format21)
        sheet.merge_range(4, 15, 2, 16, 'Tổng muộn', format21)
        sheet.merge_range(4, 17, 2, 18, 'Số công', format21)
        sheet.merge_range(4, 19, 2, 20, 'Ghi chú', format21)
        # c = 7
        # for i in range(32):
        #     c = c + 1
        #     sheet.merge_range(1, c, 2,c, i + 1, font_size_8_l)
            
        # sheet.merge_range(1, 8, , 8, "hello", format21)


        get_line = self.get_lines(lines)
        prod_row = 5
        prod_col = 0
        for each in get_line:
            # sheet.merge_range(1, 6, 4, 7, str(get_line), format21)
            total = 0
            check_out = '{0:02.0f}:{1:02.0f}'.format(*divmod( each['check_out'] * 60, 60))
            check_in = '{0:02.0f}:{1:02.0f}'.format(*divmod(each['check_in'] * 60, 60))
            date = str(each['date'].strftime("%Y-%m-%d"))
            if each['check_out'] >= 17.5 and each['check_in'] <= 8.5:
                total = 1
            else:
                total = 0.5
            # sheet.merge_range(prod_row, prod_col , prod_row, prod_col, "1", font_size_8_l)
            sheet.merge_range(prod_row, prod_col + 0, prod_row, prod_col + 2, each['employee_id'], font_size_8_l)
            sheet.merge_range(prod_row, prod_col + 3, prod_row, prod_col + 4, each['department'], font_size_8)
            sheet.merge_range(prod_row, prod_col + 5, prod_row, prod_col + 6, each['method_work'], font_size_8)
            sheet.merge_range(prod_row, prod_col + 7, prod_row, prod_col + 8, date, font_size_8)
            
            sheet.merge_range(prod_row, prod_col + 9, prod_row, prod_col + 10, Const._get_day_of_date(each['date']), font_size_8)
            sheet.merge_range(prod_row, prod_col + 11, prod_row, prod_col + 12, check_in, font_size_8)
            sheet.merge_range(prod_row, prod_col + 13, prod_row, prod_col + 14, check_out, font_size_8)
            sheet.merge_range(prod_row, prod_col + 15, prod_row, prod_col + 16, "", font_size_8)
            sheet.merge_range(prod_row, prod_col + 17, prod_row, prod_col + 18, total, font_size_8)
            sheet.merge_range(prod_row, prod_col + 21, prod_row, prod_col + 20, "", font_size_8)
            prod_row = prod_row + 1

        # sheet.merge_range(0, 0, 0, 20, 'Tên công ty: Công ty TNHH Rabiloo ' , format4)
        																																							
        # sheet.merge_range(1, 0, 1, 20, 'Địa chỉ: Tầng 5, A3, Ecolife Capital, 58 Tố Hữu, Trung Văn, Nam Từ Liêm, Hà Nội' , format4)
        # sheet.merge_range(4, 7, 3, 10, 'Bảng chấm công', format0)

        # sheet.merge_range(5, 7, 5, 10, 'Từ ngày ' + str(times.strftime("%Y-%m-%d %H:%M %p")), format11)
        # for obj in lines:
        #     name = lines.employee_id.name        
            # sheet.merge_range(0, 0, 0, 20, name, format11)

        # sheet.merge_range(7, 7, 7, count, 'Warehouses', format1)
        # sheet.write()
        #  sheet.merge_range(2, 7, 3, 10, date, format11)
        # d1 = d.mapped('id')
        # print("d1",d1)