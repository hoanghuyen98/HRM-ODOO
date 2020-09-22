from odoo import models
import calendar
import pytz
from . import Const
from . import working_shift
import xlsxwriter
from odoo import models, fields, api,  _
from datetime import datetime, date
class CheckingALLXlsx(models.AbstractModel):
    _name = 'report.employees.report_all_checking_xls'
    _inherit = 'report.report_xlsx.abstract'
    
         
    def get_lines(self, data, employee_id):
        lines = []
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
            SELECT employees_checking.employee_id,date, max(time_checking), min(time_checking) FROM employees_checking 
            WHERE date >= %(start_date)s
            AND  date <= %(end_date)s
            AND employees_checking.employee_id = %(employee_id)s
            GROUP BY date, employees_checking.employee_id 
            ORDER BY  date
            """

        params = {
            "start_date": data.start_date,
            "end_date": data.end_date,
            "employee_id": employee_id
        }

        self._cr.execute(employee_query, params)
        sol_query_obj = self._cr.dictfetchall()
        for item in sol_query_obj:
            employee = self.env['employees.employee'].search([('id', '=', item['employee_id'])])
            if employee is None:
                raise Exception("Employee not found")
            shift = working_shift.get_report_of_employee_by_date(employee, item['date'], item['min'], item['max'] )
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

        sheet = workbook.add_worksheet("Bảng chấm công")

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
 
        sheet.merge_range(7, 16, 8, 17, 'Chấm công', merge_format)
        
        sheet.merge_range(0, 0, 0, 20, 'Tên công ty: Công ty TNHH Rabiloo ' , format4)
        sheet.merge_range(1, 0, 1, 20, 'Địa chỉ: Tầng 5, A3, Ecolife Capital, 58 Tố Hữu, Trung Văn, Nam Từ Liêm, Hà Nội' , format4)
        sheet.merge_range(3, 5, 4, 15, 'Bảng Chấm Công', format0)
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        start_date = str(lines.start_date.strftime("%Y-%m-%d"))
        end_date = str(lines.end_date.strftime("%Y-%m-%d"))
        monthRange_day = working_shift.days_between(start_date, end_date)
        y = str(lines.start_date.strftime("%Y"))
        d = str(lines.start_date.strftime("%m"))
        c = 8
        array_location_day = []
        for i in range(monthRange_day+1):
            new_date = ""
            number_day = str(i+1).zfill(2)
            new_date += str(y) + "-" + str(str(d).zfill(2)) + "-" + str(number_day) 
            sheet.merge_range(7, c, 8, c, number_day, merge_format)
            day_ = Const._get_day_of_date(datetime.strptime(new_date, "%Y-%m-%d"))
            location = {
                "date": new_date,
                "c": c
            }
            # sheet.merge_range(7, c, 7, c, day_, merge_format)
            array_location_day.append(location)
            c = c + 1
            

        prod_row = 9
        prod_col = 0

       
        employee_query = """
            SELECT name, id FROM employees_employee 
            ORDER BY  id
            """
        self._cr.execute(employee_query)
        sol_query_obj = self._cr.dictfetchall()
        for em in sol_query_obj:
            get_line = self.get_lines(lines, em['id'] )
            for each in get_line:

                
                # date = str(each['date'].strftime("%Y-%m-%d"))

                sheet.write(prod_row, 0, str(get_line), font_size_8_l)
                
                
                # sheet.merge_range(prod_row, prod_col , prod_row, prod_col, each['name'], font_size_8_l)
                sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name_seq'], font_size_8_l)
                sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['department'], font_size_8)
                sheet.merge_range(prod_row, prod_col + 6, prod_row, prod_col + 7, each['method_work'], font_size_8)
                for i in range(len(array_location_day)):
                    shift = ""

                    if each['shift'] == 1:
                        shift = "x" 
                    elif each['shift'] == 0.5:
                        shift = "x/2"
                    if str(array_location_day[i]['date']) == str(each['date']):
                        sheet.write(prod_row, array_location_day[i]['c'],shift, font_size_8)
                    # else: 
                    #     sheet.write(prod_row, array_location_day[i]['c'], "" , font_size_8)

                # sheet.merge_range(prod_row, prod_col + 16, prod_row, prod_col + 17, each['shift'], font_size_8)

                # sheet.merge_range(prod_row, prod_col + 17, prod_row, prod_col + 18, total, font_size_8)
                # sheet.merge_range(prod_row, prod_col + 21, prod_row, prod_col + 20, "", font_size_8)
            prod_row = prod_row + 1
