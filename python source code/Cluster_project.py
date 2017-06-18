# -*- coding: utf-8 -*-
class Cluster_project(object):
    def __init__(self, idProject, idCluster):
        #idCluster - массив id кластеров, соответствующих данному проекту
        self.idProject = idProject
        self.idCluster = idCluster