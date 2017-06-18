# -*- coding: utf-8 -*-
class Cluster(object):
    def __init__(self, idCluster, percentageHasSTR, percentageHasEOB,
                 percentageHasConfigFilesOrLogs, percentageHasImages,
                 percentageHasStackTrace, percentageHasJavaCode,
                 percentageBugsInClusterInProject, wordsInClusterRankedByTfidf):
        self.idCluster = idCluster
        self.percentageHasSTR = percentageHasSTR
        self.percentageHasEOB = percentageHasEOB
        self.percentageHasConfigFilesOrLogs = percentageHasConfigFilesOrLogs
        self.percentageHasImages = percentageHasImages
        self.percentageHasStackTrace = percentageHasStackTrace
        self.percentageHasJavaCode = percentageHasJavaCode
        self.percentageBugsInClusterInProject = percentageBugsInClusterInProject
        self.wordsInClusterRankedByTfidf = wordsInClusterRankedByTfidf