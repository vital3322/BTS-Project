# -*- coding: utf-8 -*-
import pandas as pd
import Bug

class Project(object):
    def __init__(self, idProject):
        self.idProject = idProject
        self.nameProject = "Project_%d" % int(idProject)
        self.project_csv_filename
        self.bugList = list()
    
    def read_project_csv(self, filename):
        self.bugList = list()
        newBugID = 1
        for line_data in file_data:
            newBug = Bug(newBugID, self.idProject, line_data.rawBugDescription)
            self.bugList.append(newBug)
            newBugID += 1
        
        col_attachments = list()
        col_attachments_1 = list()
        col_num_of_comments = list()
        arr_time_created_for_all_projects = list()
        arr_time_resolved_for_all_projects = list()
        number_of_bug_descr = list()
        list_total_texts = list()
        list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags = list()
        list_of_vectorized_bugs = list()
        
        data = pd.read_csv(filename)    
        
        cols=pd.Series(data.columns)
        for dup in data.columns.get_duplicates(): cols[data.columns.get_loc(dup)]=[dup+'.'+str(d_idx) if d_idx!=0 else dup for d_idx in range(data.columns.get_loc(dup).sum())]
        data.columns = cols
        
        data.dropna(subset = ['Description'], inplace = True)
        time_created = list(data['Created'][1:])
        
        attachment = list(data['Attachment'][1:])
        col_attachments.append(attachment)
        attachment_1 = list(data['Attachment.1'][1:])
        col_attachments_1.append(attachment_1)
        col_num_comm = list(data['Custom field (Number of comments)'][1:])
        col_num_of_comments.append(col_num_comm)
        
        arr_time_created_for_all_projects = arr_time_created_for_all_projects + time_created
        time_resolved = list(data['Resolved'][1:])
        arr_time_resolved_for_all_projects = arr_time_resolved_for_all_projects + time_resolved
        
        data_description0 = data['Description'][1:]
        data_description0.to_frame()
        data_len = len(data_description0)
        number_of_bug_descr.append(data_len)
        zeros_df = pd.DataFrame(0, index=data_description0.index, columns=['HasStackTrace'])
        data_description = pd.concat([data_description0, zeros_df], axis=1)
        
        subset = data_description[['Description', 'HasStackTrace']]
        list_of_bugs_descriptions_and_stack_trace_flags = [list(x) for x in subset.values]
                                                           
        
        for k,item in enumerate(list_of_bugs_descriptions_and_stack_trace_flags):
            text = item[0]
            list_total_texts.append(text)
            list_of_bugs_descriptions_and_stack_trace_flags[k] = filter_pattern(arr_patterns, text) 
            
            
        list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags = list_of_all_projects_cleaned_bugs_descriptions_with_stack_trace_flags + list_of_bugs_descriptions_and_stack_trace_flags
        for num, item in enumerate(list_of_bugs_descriptions_and_stack_trace_flags): 
            list_of_vectorized_bugs.append([self.idProject, num, item[1], 0, 0, 0])
    
            
    def preprocessing_text(self):
        for bug in self.bugList:
            bug.obrabotka()
    
    def mark_ETR_and_EOB(self, mark_dict):
        for bug in self.bugList:
            bug.STR = mark_dict[bug.idBug].STR
            bug.EOB = mark_dict[bug.idBug].EOB
