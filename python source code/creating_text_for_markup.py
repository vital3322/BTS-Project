# -*- coding: utf-8 -*-
import xlwt
import pandas as pd

def creating_text_for_markup(project_file_name):
    style1 = xlwt.XFStyle()
    style1.num_format_str = 'D-MMM-YY'
    style1.alignment.wrap = 1
    
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    
    ws.write(0, 0, 'document_id', style1)
    ws.write(0, 1, 'description_id', style1)
    ws.write(0, 2, 'description', style1)
    ws.write(0, 3, 'steps to reproduce', style1)
    ws.write(0, 4, 'expected/observed behavior', style1)
    
    ws.col(0).width = 3200 # In pixels
    ws.col(1).width = 3200 # In pixels
    ws.col(2).width = 30000 # In pixels
    ws.col(3).width = 5000 # In pixels
    ws.col(4).width = 6500 # In pixels
    
    number_of_bug_descr = list()
    data_len_sum = 0
    data = pd.read_csv(project_file_name)
    
    data_description0 = data['Description'][1:]
    data_description0.dropna(inplace = True)
    data_description0.to_frame()
    data_len = len(data_description0)
    
    number_of_bug_descr.append(data_len)
    index = 1
    for item in data_description0:
        ws.write(data_len_sum + index, 0, i)
        ws.write(data_len_sum + index, 1, index)
        len_item = len(item)
        if len(item) >= 32766:
            ws.write(data_len_sum + index, 2, item[:32766], style1)
        else :
            ws.write(data_len_sum + index, 2, item, style1)
        index += 1
    data_len_sum += data_len
    
    wb.save('example.xls')