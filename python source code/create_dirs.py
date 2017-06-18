# -*- coding: utf-8 -*-
from shutil import copyfile
import os
def load_project_in_system():
    raw_file = input('Input path to csv file with raw bug reports (with file name): ')
    if os.path.isfile(raw_file):
        maximum = 0
        for file in os.listdir('Projects'):
            #if file.endswith(".csv"):
            project_num = int(os.path.join(file).split('_')[1])
            if project_num > maximum:
                maximum = project_num
        new_directory = 'Projects/Project_'+str(maximum+1)        
        os.makedirs(new_directory)   
        copyfile(raw_file, new_directory+'/original_csv_'+str(maximum+1)+'.csv')     
        os.makedirs(new_directory+'/Configurations')  
        open(new_directory+'/Configurations/raw_description.txt', 'a').close()
        open(new_directory+'/Configurations/processed_description.txt', 'a').close()
        open(new_directory+'/Configurations/parameters.txt', 'a').close()
        #preprocessing(new_directory+'/original_csv_'+str(maximum+1)+'.csv')
        return True
    print('No such file: %s' %raw_file)
    return False

load_project_in_system()