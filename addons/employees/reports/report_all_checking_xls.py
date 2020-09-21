from odoo import models
import calendar
import pytz
from . import Const
from odoo import models, fields, api,  _
from datetime import datetime, date
class CheckingXlsx(models.AbstractModel):
    _name = 'report.employees.report_all_checking_xls'
    _inherit = 'report.report_xlsx.abstract'
    

    # def get_lines(self, data):
    #     lines = []
    #     employee_ids = data.employee_id.mapped('id')
    #     if employee_ids:
    #         employee = self.env['employees.checking'].search([('employee_id', 'in', employee_ids)])

    #     else:
    #         employee = self.env['employees.checking'].search([])
        
    #     employee_query = """
    #         SELECT date, employee_id, max(time_checking), min(time_checking) FROM employees_checking 
    #         GROUP BY employee_id , date
    #         ORDER BY  employee_id ASC;
    #         """
    #     params = {"employee_id": employee_ids}
    #     self._cr.execute(employee_query, params)
    #     sol_query_obj = self._cr.dictfetchall()

    #     list_employee_repory = []
    #     records = 0
    #     for item in sol_query_obj:
    #         check_in = 0
    #         check_out = 0
    
    #         for obj in employee:
    #             if int(item['employee_id']) == obj.employee_id.id:
    #                 seen = set()
    #                 new_l = []
                   
    #                 vals = {
    #                     'id': obj.employee_id.name,
    #                     'employee_id': str(employee_ids),
    #                     'department': obj.employee_id.department_id.name,
    #                     'method_work': obj.employee_id.method_work,
    #                     'check_in': item['min'],
    #                     'check_out': item['max'],
    #                 }
                        
    #                 lines.append(vals)
    #                 break
            
    #     return lines

    def generate_xlsx_report(self, workbook, data, lines):

        sheet = workbook.add_worksheet('Chấm công')    
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
        merge_format = workbook.add_format({
            # 'bold': 1,
            # 'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            # 'fg_color': 'yellow'
        })

        sheet.merge_range(0, 0, 0, 20, 'Tên công ty: Công ty TNHH Rabiloo ' , format4)
        sheet.merge_range(1, 0, 1, 20, 'Địa chỉ: Tầng 5, A3, Ecolife Capital, 58 Tố Hữu, Trung Văn, Nam Từ Liêm, Hà Nội' , format4)
        sheet.merge_range(3, 5, 4, 15, "Bảng chấm công", format0)
        sheet.merge_range(15, 0, 18, 0, 'STT', merge_format)
        sheet.merge_range(15, 1, 18, 2, str(workbook), merge_format)
        sheet.merge_range(15, 3, 18, 4, str(data), merge_format)
        sheet.merge_range(15, 5, 18, 6, str(lines[0]), merge_format)

        sheet.merge_range(7, 3, 8, 20, "Ký hiệu     X: Đủ công      X/2: Nửa công      P: Nghỉ phép      NL: Nghỉ lễ      OT: Tăng ca      N: Nghỉ thường", format21)
        

        # month = ""
        # d = 0
        # y = 0
        # get_line = self.get_lines(lines)
        # prod_row = 19
        # prod_col = 0
        # count = 1
        # employee_id = lines.employee_id.mapped('id')
        # if employee_id:
        #     date = self.env['employees.checking'].search([('employee_id', 'in', employee_id)])[0].date

        # else:
        #     date = self.env['employees.checking'].search([])
        
        # for each in get_line:
        #     month = str(date.strftime("Tháng %m năm %Y"))
        #     d = int(date.strftime("%m"))
        #     y = int(date.strftime("%Y"))
            
        #     sheet.write(prod_row, 0, count, font_size_8)
        #     sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 2, each['employee_id'], font_size_8_l)
        #     sheet.merge_range(prod_row, prod_col + 3, prod_row, prod_col + 4, each['department'], font_size_8)
        #     sheet.merge_range(prod_row, prod_col + 5, prod_row, prod_col + 6, each['method_work'], font_size_8)
            
        #     prod_row = prod_row + 1
        #     count = count + 1
        # sheet.merge_range(5, 5, 5, 15, month, format21)

        # monthRange_day = Const.number_of_days(d, y)

        # c = 7
        # prod_row = 19
        # prod_col = 0
        # for i in range(monthRange_day):
        #     new_date = ""
        #     number_day = str(i+1).zfill(2)
        #     new_date += str(y) + "-" + str(str(d).zfill(2)) + "-" + str(number_day) 
        #     sheet.merge_range(15, c, 16, c, number_day, merge_format)
        #     day_ = Const._get_day_of_date(new_date)
        #     sheet.merge_range(17, c, 18, c, day_, merge_format)

        #     c = c + 1
        #     prod_row = prod_row + 1
