# -*- coding: utf-8 -*-
import os
from shutil import copyfile
import Parameters
import xlwt
import pandas as pd

class Bts_plug_in_system(object):
# *** static class data ***     
    roles = {
        '1' : 'admin',
        '2' : 'analyst',
        '3' : 'user'
    }
# *** object data ***

    def __init__(self):
        self.list_of_projects = list()
        self.list_of_bugs = list()
        self.list_of_clusters = list()
        self.list_of_recommendations = list()
        self.role = "user"
        print("The Bag Report Quality Predictor.")
        print("======================================================================\n")

# *** Main Functions ***       
    
    def choose_the_action(self):
        if self.role == "admin":
            action = input(Bts_plug_in_system.get_admin_action_instructions())
            if  action == "1":
                return "load_project_in_system"
            if  action == "2":
                return "system_learning"
            if  action == "3":
                return "create_recommendations"
            
        if self.role == "analyst":
            action = input(Bts_plug_in_system.get_analyst_action_instructions())
            if  action == "1":
                return "setting_system_params"
            if  action == "2":
                return "show_project_list"
            if  action == "3":
                return "show_project_params"
            if  action == "4":
                return "export_excel_file_for_STR_EOB_marking"
            if  action == "5":
                return "import_excel_file_for_STR_EOB_marking"
        if self.role == "user":
            action = input(Bts_plug_in_system.get_user_action_instructions())
            if  action == "1":
                return "load_bug_and_get_recommendations"
        
    def load_project_in_system(self):
        print("\nload_project_in_system:")
        raw_file = input('Input path to csv file with raw bug reports (with file name): ')
        while not os.access(raw_file, os.W_OK):
            print("Error, not exist %s" % raw_file)
            raw_file = input('Please input correct path to csv file with raw bug reports (with file name): ')    
        maximum = 0
        if not 'Projects' in os.listdir('./'):
            os.makedirs('Projects')
        for file in os.listdir('Projects'):
            #if file.endswith(".csv"):
            project_num = int(os.path.join(file).split('_')[1])
            if project_num > maximum:
                maximum = project_num
        new_directory = 'Projects/Project_'+str(maximum+1)        
        os.makedirs(new_directory)   
        copyfile(raw_file, new_directory+'/original_csv_'+str(maximum+1)+'.csv')     
        os.makedirs(new_directory+'/Configurations')  
        open(new_directory+'/Configurations/raw_description_%d.txt'  % (maximum + 1), 'a').close()
        open(new_directory+'/Configurations/processed_description_%d.txt'  % (maximum + 1), 'a').close()
        open(new_directory+'/Configurations/parameters_%d.txt'  % (maximum + 1), 'a').close()
        parameters = Parameters.Parameters()
        parameters.write_parameters_to_file(new_directory+'/Configurations/parameters_%d.txt' % (maximum + 1))
        
#        Bug.preprocessing_text(new_directory+'/original_csv_'+str(maximum+1)+'.csv')
    
    def system_learning(self):
        print("\nAction system_learning undefined\n")
        
    def create_recommendations(self):
        print("\nAction create_recommendations undefined\n")
    
    def choose_project(self):
        instruction = "\nChoose Project:\n"
        project_num_list_str = "\nSelect a action and press ENTER ["
        project_list = sorted(os.listdir('Projects'), key =lambda file: int(os.path.join(file).split('_')[1]))
        max_project_num = len(os.path.join(project_list[-1]).split('_')[1])
        i = 0
        for file in project_list:
            project_num = os.path.join(file).split('_')[1]
            project_num_list_str += project_num
            if i < len(project_list) - 1:
                project_num_list_str += "/"
            project_num_str_option = "[%s]" % (project_num)    
            instruction += "%*s Project %s\n" % (max_project_num + 2, project_num_str_option, project_num)
            i += 1
        project_num_list_str += "]: "
        instruction += project_num_list_str
        
        idProject = input(instruction)
        return int(idProject)
        
    def setting_system_params(self):
        idProject = int(self.choose_project())
        
        parameters = Parameters.Parameters()
       
        parameters.set_parameters(idProject)
        
    def show_project_list(self): #аргумент - id проекта
        instruction = "\nProject List: \n"
        project_list = sorted(os.listdir('Projects'), key =lambda file: int(os.path.join(file).split('_')[1]))
        max_project_num = len(os.path.join(project_list[-1]).split('_')[1])

        for file in project_list:
            project_num = os.path.join(file).split('_')[1]
            project_num_str_option = "[%s]" % (project_num)    
            instruction += "%*s Project %s\n" % (max_project_num + 2, project_num_str_option, project_num)
        print(instruction)
        
        return   
    
    def show_project_params(self): #аргумент - id проекта
        idProject = self.choose_project()
        parameters = Parameters.Parameters()
        parameter_list = parameters.read_parameters(idProject)
        output = "\nParameters for Project_%d: \n\n" % idProject
        for param in parameter_list:
            output += "  %s = %s\n" % (param[0], param[1])
        
        print(output)
            
    def export_excel_file_for_STR_EOB_marking(self):
        idProject = self.choose_project()
        project_file_name = "Projects/Project_%d/original_csv_%d.csv" % (idProject, idProject)
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
            ws.write(data_len_sum + index, 0, idProject)
            ws.write(data_len_sum + index, 1, index)
            if len(item) >= 32766:
                ws.write(data_len_sum + index, 2, item[:32766], style1)
            else :
                ws.write(data_len_sum + index, 2, item, style1)
            index += 1
        data_len_sum += data_len
        save_file_name = 'Projects/Project_%d/export_STR_EOB_marking_%d.xls' % (idProject, idProject)
        wb.save(save_file_name)
        
        print("\n" + save_file_name + " successfully exported\n")
        
    def import_excel_file_for_STR_EOB_marking(self):
        idProject = self.choose_project()
        print("\nimport_xls_for_STR_EOB_marking:")
        source_file = input('Input path to xls file with STR_EOB_marking (with file name): ')
        while not os.access(source_file, os.W_OK):
            print("Error, not exist %s" % source_file)
            source_file = input('Please input correct path to xls file with STR_EOB_marking (with file name): ')  
        dest_file = 'Projects/Project_%d/import_STR_EOB_marking_%d.xls' % (idProject, idProject)
        copyfile(source_file, dest_file)     

        
        
    def load_bug_and_get_recommendations(self):
        print("\nAction load_bug_and_get_recommendations undefined\n")
        
    def continue_or_save_or_exit(self):
        action_program = input('If you want to exit, press key "Q"\nIf you want to continue, press key "C": ')
        if (action_program in ['q','Q']):
            return True
        if (action_program in ['c','C']):
            return False

# input and set role by using Console User Interface    '
# @return str(role)   
    def who_are_you(self):
        while(True):
            role_instruction = Bts_plug_in_system.get_role_instructions()
            role = input(role_instruction)
            if(role in Bts_plug_in_system.roles.keys()):
                self.role = Bts_plug_in_system.roles[role]
                print("Role successfuly set to \"", self.role, "\"\n")
                return self.role
            print("\nError: Incorrect input data!")
            print("\nPlease, select role again.\n")

# *** Supporting Functions ***   

    @staticmethod
    def get_role_instructions():
        role_instruction = "Available roles:\n"
        roles_sorted_by_key = sorted(Bts_plug_in_system.roles.items())
        for key_role, role in roles_sorted_by_key:
            role_instruction += "[" + key_role + "] " + role + "\n"
        role_instruction += "\nSelect a role and press ENTER ["
        for key_role, role in roles_sorted_by_key:
            role_instruction += key_role
            if int(key_role) < len(roles_sorted_by_key):
                role_instruction += "/"
        role_instruction += "]: "
        return role_instruction
        
    @staticmethod
    def get_admin_action_instructions():
        instruction = "Admin actions:\n"
        instruction += "[1] load_project_in_system\n"
        instruction += "[2] system_learning\n"
        instruction += "[3] create_recommendations\n"
        instruction += "\nSelect a action and press ENTER [1/2/3]: "
        return instruction

    @staticmethod
    def get_analyst_action_instructions():  
        instruction = "Analyst actions:\n"
        instruction += "[1] setting_system_params\n"
        instruction += "[2] show_project_list\n"
        instruction += "[3] show_project_params\n"
        instruction += "[4] export_excel_file_for_STR_EOB_marking\n"
        instruction += "[5] import_excel_file_for_STR_EOB_marking\n"
        instruction += "\nSelect a action and press ENTER [1/2/3/4/5]: "
        return instruction
    
    @staticmethod
    def get_user_action_instructions():  
        instruction = "USer actions:\n"
        instruction += "[1] load_bug_and_get_recommendations\n"
        instruction += "\nSelect a action and press ENTER [1]: "
        return instruction
        
    