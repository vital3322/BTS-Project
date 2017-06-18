# -*- coding: utf-8 -*-
import os
import json
import csv

def write_json(data, filename):
    #'posts.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def write_csv(dict_data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in dict_data.items():
           writer.writerow([key, value])

def read_csv(filename):
    reader = csv.reader(open(filename, "r")) 
    result = list()
    for row in reader:
        if len(row) != 0:
            result.append(row)
    return result
            
class Parameters():
    
    def __init__(self):
        self.numClustersForFirstStep = 12
        self.numClustersForSecondStep = 18
        self.numWordsWithMaxTfidf = 100
        self.percentWordsFromClusterToExpandFeatures = 50
        self.percentSTRtoDecideSTR = 10
        self.percentEOBtoDecideEOB = 10
    
    def set_numClustersForFirstStep(self, new_numClustersForFirstStep):
        self.numClustersForFirstStep = new_numClustersForFirstStep
        
    def set_numClustersForSecondStep(self, new_numClustersForSecondStep):
        self.numClustersForSecondStep = new_numClustersForSecondStep
        
    def set_numWordsWithMaxTfidf(self, new_numWordsWithMaxTfidf):
        self.numWordsWithMaxTfidf = new_numWordsWithMaxTfidf
        
    def set_percentWordsFromClusterToExpandFeatures(self, new_percentWordsFromClusterToExpandFeatures):
        self.percentWordsFromClusterToExpandFeatures = new_percentWordsFromClusterToExpandFeatures
        
    def set_percentSTRtoDecideSTR(self, new_percentSTRtoDecideSTR):
        self.percentSTRtoDecideSTR = new_percentSTRtoDecideSTR
        
    def set_percentEOBtoDecideEOB(self, new_percentEOBtoDecideEOB):
        self.percentEOBtoDecideEOB = new_percentEOBtoDecideEOB
        
    def write_parameters_to_file(self, filepath):
        file = open(filepath, 'w', encoding='utf-8')
        file.close()
        data_dict = {
            "numClustersForFirstStep": self.numClustersForFirstStep,
            "numClustersForSecondStep": self.numClustersForSecondStep,
            "numWordsWithMaxTfidf": self.numWordsWithMaxTfidf,
            "percentWordsFromClusterToExpandFeatures": self.percentWordsFromClusterToExpandFeatures,
            "percentSTRtoDecideSTR": self.percentSTRtoDecideSTR,
            "percentEOBtoDecideEOB": self.numClustersForFirstStep,
        }
        
        write_csv(data_dict, filepath)
        
    def print_all_parameters(self):
        parameters_str = "numClustersForFirstStep: %d" % (self.numClustersForFirstStep)
        parameters_str += "numClustersForSecondStep: %d" % (self.numClustersForSecondStep)
        parameters_str += "numWordsWithMaxTfidf: %d" % (self.numWordsWithMaxTfidf)
        parameters_str += "percentWordsFromClusterToExpandFeatures: %d" % (self.percentWordsFromClusterToExpandFeatures)
        parameters_str += "percentSTRtoDecideSTR: %d" % (self.percentSTRtoDecideSTR)
        parameters_str += "percentEOBtoDecideEOB: %d" % (self.percentEOBtoDecideEOB)
        print(parameters_str)
    
    def set_parameters(self, idProject):
        print("\nSet Parameters for Project_%d:\n" % idProject)
        new_numClustersForFirstStep = input('Input new value for numClustersForFirstStep (1/6): ')
        new_numClustersForSecondStep = input('Input new value for numClustersForSecondStep (2/6): ')
        new_numWordsWithMaxTfidf = input('Input new value for numWordsWithMaxTfidf (3/6): ')
        new_percentWordsFromClusterToExpandFeatures = input('Input new value for percentWordsFromClusterToExpandFeatures (4/6): ')
        new_percentSTRtoDecideSTR = input('Input new value for percentSTRtoDecideSTR (5/6): ')
        new_percentEOBtoDecideEOB = input('Input new value for percentEOBtoDecideEOB (6/6): ')
  
        self.set_numClustersForFirstStep(new_numClustersForFirstStep)
        self.set_numWordsWithMaxTfidf(new_numClustersForSecondStep)
        self.set_numClustersForSecondStep(new_numWordsWithMaxTfidf)
        self.set_percentWordsFromClusterToExpandFeatures(new_percentWordsFromClusterToExpandFeatures)
        self.set_percentSTRtoDecideSTR(new_percentSTRtoDecideSTR)
        self.set_percentEOBtoDecideEOB(new_percentEOBtoDecideEOB)
        
        paremeters_filename = "Projects/Project_%d/Configurations/parameters_%d.txt" % (idProject, idProject)
        self.write_parameters_to_file(paremeters_filename)
        print("\nAll Parameters succeessfully sets for Project_%d:\n" % idProject)
        
    def get_parameters(self):
        for file in os.listdir('Projects'):
            print(os.path.join(file))
        project_name = input('To choose project input name of it: ')
        with open('Projects/' + project_name +'/Configurations/Parameters.txt', 'r') as f:
            for line in f:
                print(line)
        answer = input('Do you want to change parameters? Press y/n: ')
        if answer == 'y':
            self.set_parameters(project_name)
        
        parameter = Parameters()
        parameter.set_value(11)
        Parameters.write_to_file("Project1/parametrs.txt")
        print(Parameters)
        
    def read_parameters(self, idProject):
        filename = 'Projects/Project_%d/Configurations/parameters_%d.txt' % (idProject, idProject)
        return read_csv(filename)
        