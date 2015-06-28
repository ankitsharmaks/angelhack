from math import ceil
from operator import itemgetter

MaxRec = 6

def normalizeRank(tagsWithScore,recall):
    newtagList = []
    totalRecCount = 0
    for tag in tagsWithScore:
        tag[1] = ceil(tag[1]*recall)
        totalRecCount +=tag[1]
        if totalRecCount < MaxRec:
            newtagList.append(tag)
        else:
            tag[1] = MaxRec - (totalRecCount - tag[1])
            newtagList.append(tag)
            return newtagList
    return newtagList

def getCountForTags(tagsWithScore):
    scoreSum = 0
    for tag in tagsWithScore:
        scoreSum +=tag[1]
    if scoreSum>0:
        recall = MaxRec/scoreSum
    else:
        tagsWithScore[0][1] = MaxRec
        return tagsWithScore
    return normalizeRank(tagsWithScore,recall)
