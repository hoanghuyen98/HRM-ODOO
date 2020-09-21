from odoo import models
import calendar
import pytz
from . import Const
from . import working_shift
import xlsxwriter
from odoo import models, fields, api,  _
from datetime import datetime, date
class CheckingALLXlsx(models.AbstractModel):
    _name = 'report.employees.report_checking_xls'
    _inherit = 'report.report_xlsx.abstract'
    
         
    def get_lines(self, data):
        lines = []
        ids = []
        # # id = data.id
        # employee_ids = employees.mapped("id")
        # if not employee_ids or len(employee_ids) == 0:
        #      raise Exception("Employee not found")

        # employee_id = employee_ids[0]
        # employee = self.env['employees.checking'].search([('employee_id', '=', employee_id)])
        # if employee is None:
        #     raise Exception("Employee not found")
            # employee = self.env['employees.checking'].search([])
        
        employee_query = """
            SELECT employees_checking.employee_id, date, max(time_checking), min(time_checking) FROM employees_checking 
            WHERE date >= %(start_date)s
            AND  date <= %(end_date)s
            AND  employees_checking.employee_id in %(list_employee)s
            GROUP BY date, employees_checking.employee_id 
            ORDER BY  date
            """
        for employee in  data.employee_line:
            ids.append(employee.employee_name.id)

        params = {
            "start_date": data.start_date,
            "end_date": data.end_date,
            "list_employee": tuple(ids)
        }

        self._cr.execute(employee_query, params)
        sol_query_obj = self._cr.dictfetchall()
        for item in sol_query_obj:
            employee = self.env['employees.employee'].search([('id', '=', item['employee_id'])])
            if employee is None:
                raise Exception("Employee not found")
            shift = working_shift.get_report_of_employee_by_date(employee,item['date'], item['min'], item['max'] )
            vals = {
                'id': employee[0].id,
                'name': employee[0].name,
                'name_seq': employee[0].name_seq,
                'department': employee[0].department_id.name,
                'method_work': employee[0].method_work,
                'status_work': employee[0].status_work,
                'shift': shift,
                'check_out': item['max'],
                'check_in': item['min'],
                'date': item['date'],             
            }
            lines.append(vals)        

        return lines

    def generate_xlsx_report(self, workbook, data, lines):

        for em in  lines.employee_line:
            try:
                sheet = workbook.add_worksheet(em.employee_name.name_seq)
            except xlsxwriter.exceptions.DuplicateWorksheetName:
                sheet = workbook.get_worksheet_by_name(em.employee_name.name_seq)
                # worksheet = workbook.get_worksheet_by_name(sheetName)
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
            sheet.merge_range(7, 0, 8, 0, 'Mã NV', merge_format)
            sheet.merge_range(7, 1, 8, 3, 'Họ tên', merge_format)
            sheet.merge_range(7, 4, 8, 5, 'Team', merge_format)
            sheet.merge_range(7, 6, 8, 7, 'Trạng thái', merge_format)
            sheet.merge_range(7, 8, 8, 9, 'Ngày', merge_format)
            sheet.merge_range(7, 10, 8, 11, 'Thứ', merge_format)
            sheet.merge_range(7, 12, 8, 13, 'Giờ đến', merge_format)
            sheet.merge_range(7, 14, 8, 15, 'Giờ về', merge_format)
            sheet.merge_range(7, 16, 8, 17, 'Chấm công', merge_format)
            
            sheet.merge_range(0, 0, 0, 20, 'Tên công ty: Công ty TNHH Rabiloo ' , format4)
            sheet.merge_range(1, 0, 1, 20, 'Địa chỉ: Tầng 5, A3, Ecolife Capital, 58 Tố Hữu, Trung Văn, Nam Từ Liêm, Hà Nội' , format4)
            sheet.merge_range(3, 5, 4, 15, 'Bảng Chấm Công', format0)
            format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
            format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
    
            prod_row = 9
            prod_col = 0
            get_line = self.get_lines(lines)

            for each in get_line:
                if each['id'] == em.employee_name.id:
                    check_out = '{0:02.0f}:{1:02.0f}'.format(*divmod( each['check_out'] * 60, 60))
                    check_in = '{0:02.0f}:{1:02.0f}'.format(*divmod(each['check_in'] * 60, 60))
                    date = str(each['date'].strftime("%Y-%m-%d"))

                    sheet.write(prod_row, 0, each['name'], font_size_8_l)
                    schedule = self.env['employees.scheduler'].search([('time_start', '>=',each['check_in'])])
                    schedule_end = schedule.search([('time_finish', '<=',each['check_out'])])
                    
                    # sheet.merge_range(prod_row, prod_col , prod_row, prod_col, each['name'], font_size_8_l)
                    sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name_seq'], font_size_8_l)
                    sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['department'], font_size_8)
                    sheet.merge_range(prod_row, prod_col + 6, prod_row, prod_col + 7, each['method_work'], font_size_8)
                    sheet.merge_range(prod_row, prod_col + 8, prod_row, prod_col + 9, date, font_size_8)
                    
                    sheet.merge_range(prod_row, prod_col + 10, prod_row, prod_col + 11, Const._get_day_of_date(each['date']), font_size_8)
                    sheet.merge_range(prod_row, prod_col + 12, prod_row, prod_col + 13, check_in, font_size_8)
                    sheet.merge_range(prod_row, prod_col + 14, prod_row, prod_col + 15, check_out, font_size_8)
                    sheet.merge_range(prod_row, prod_col + 16, prod_row, prod_col + 17, each['shift'], font_size_8)
                    # sheet.merge_range(prod_row, prod_col + 17, prod_row, prod_col + 18, total, font_size_8)
                    # sheet.merge_range(prod_row, prod_col + 21, prod_row, prod_col + 20, "", font_size_8)
                    prod_row = prod_row + 1
