# -*- coding: utf-8 -*-
class Cluster_recommendation(object):
    def __init__(self, idCluster, idRecommendation):
        #idRecommendation - массив id рекомендаций, соответствующих данному кластеру
        self.idCluster = idCluster
        self.idRecommendation = idRecommendation  