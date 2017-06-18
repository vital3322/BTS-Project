# -*- coding: utf-8 -*-
import os

class Project_parameters(object):
    def __init__(self, idProject):
        #paramsValue - объект класса Parameters
        self.idProject = int(idProject)
        self.idParameter = int(idProject)
        self.paramsValue = None
    
    def set_parameter_values(self, paramsValue):
        self.paramsValue = paramsValue
    
    def set_id_parameter(self, idParametr):
        self.idParameter = idParametr
    
    def choose_parameters(self):
        instruction = "\nChoose Parameters:\n"
        parameter_num_list_str = "\nSelect a parameter_file and press ENTER ["
        parameter_list = sorted(os.listdir('Projects'), key =lambda file: int(os.path.join(file).split('_')[1]))
        max_parameter_num = len(os.path.join(parameter_list[-1]).split('_')[1])
        i = 0
        for file in parameter_list:
            parameter_num = os.path.join(file).split('_')[1]
            parameter_num_list_str += parameter_num
            if i < len(parameter_list) - 1:
                parameter_num_list_str += "/"
            parameter_num_str_option = "[%s]" % (parameter_num)    
            instruction += "%*s parameters_%s.txt\n" % (max_parameter_num + 2, parameter_num_str_option, parameter_num)
            i += 1
        parameter_num_list_str += "]: "
        instruction += parameter_num_list_str
        
        idParameter = input(instruction)
        return int(idParameter)