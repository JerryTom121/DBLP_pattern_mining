import dataProcessing
import frequentPatternGrowth
import patternEvaluation


if __name__ == "__main__":
    
    minSupportCount = 10
    
    # Writes dblpauthorsinfo.txt file from dblpextract.txt with the author's ID, name, number of occurrence and years of publication in source seperated by \t
    # dblpauthorsinfo.txt file structure: AuthorID\tAuthor\tNumberOfOccurrenceOfAuthorIn_dblpextract.txt\n
    dataProcessing.createfileauthors("dblpextract.txt")
    
    print("Generating dictionary authorsID from dblpauthorsinfo.txt with the authors' names for keys and the associated IDs and years of publication in chronological order")
    authorsID = dataProcessing.authorsid("dblpauthorsinfo.txt")
    print("Generating done")
    print("Generating dictionary authorsName from authorsID with the authors' IDs for keys and the associated IDs and years of publication in chronological order")
    authorsName = dataProcessing.authorsname(authorsID)
    print("Generating done")
    #print(authorsID)
    #print(authorsName)
    
    # Writes dblpcoauthorsinfo.txt file from dblpextract.txt with treatises' title's IDs, year of publication, number of authors and authors' IDs seperated by \t
    # dblpcoauthorsinfo.txt file structure: TitleID\tNumberOfAuthors\tAuthorID...\n
    startYear, endYear = dataProcessing.createfilecoauthors("dblpextract.txt", authorsID)
    #print(startYear)
    #print(endYear)
    
    print("Generating dictionary database from dblpcoauthorsinfo.txt with transactions corresponding to related coauthors' IDs for keys and the associated number of occurrence and years of publication")
    database = frequentPatternGrowth.database("dblpcoauthorsinfo.txt")
    print("Generating done")
    #print(database)
    
    print("Generating dictionary frequentItems from database with the authors' IDs for keys and the associated numbers of occurrence for authors with support count superior or equal to " + str(minSupportCount))
    frequentItems = frequentPatternGrowth.frequentitems(frequentPatternGrowth.itemsoccurrence(database), minSupportCount)
    print("Generating done")
    #print(frequentItems)
    print("Generating dictionary dataSet from database for transaction with frequent items only")
    dataSet = frequentPatternGrowth.dataset(database, frequentItems)
    print("Generating done")
    #print(dataSet)
    
    print("Generating frequent pattern tree FPTree from dataSet and frequentItems")
    FPTree = frequentPatternGrowth.createFPtree(dataSet, frequentItems)
    print("Generating done")
    FPTree.printtree()

    print("Mining FPTree and generating the frequent patterns for keys and the associated support counts into dictionary frequentPatternSet")
    frequentPatternSet = { }
    frequentPatternGrowth.mineFPtree(FPTree, set([ ]), frequentPatternSet, minSupportCount)
    print("Mining done")
    print(frequentPatternSet)
    
    maxSupportCount = 0
    maxNumberCoauthors = 0
    for pattern in frequentPatternSet:
        if frequentPatternSet[pattern] > maxSupportCount:
            maxSupportCount = frequentPatternSet[pattern]
        if len(pattern) > maxNumberCoauthors:
            maxNumberCoauthors = len(pattern)
    print("%d frequent patterns found with maximum support count of %d and maximum number of coauthors of %d" %(len(frequentPatternSet), maxSupportCount, maxNumberCoauthors))
    
    patternEvaluationMeasures = patternEvaluation.PatternEvaluationMeasures(dataSet)
    print("Generating dictionary evaluatedFrequentPatternsSet from frequentPatternSet for patterns of length equal to 2")
    evaluatedFrequentPatternsSet = patternEvaluation.evaluatedfrequentpatternsset(frequentPatternSet)
    print("Generating done")
    #print(evaluatedFrequentPatternsSet)
    
    k = 10
    print("Generating frequentPatternSetSample sample of size " + str(k) + " of patterns from evaluatedFrequentPatternsSet")
    frequentPatternSetSample = patternEvaluation.frequentpatternssetsample(evaluatedFrequentPatternsSet, k)
    print("Generating done")
    #print(frequentPatternSetSample)
    # Writes frequentpatternssamplemeasures.csv and frequentpatternssamplerankings.csv files with frequentPatternSetSample evaluated and ranked by interestingness measures  
    patternEvaluation.rankfrequentpatternssamplemeasures(frequentPatternSetSample, k, authorsName, startYear, endYear, patternEvaluationMeasures)
    
    print("Generating frequentAuthorSet of authors from evaluatedFrequentPatternsSet")
    frequentAuthorSet = patternEvaluation.frequentauthorsset(evaluatedFrequentPatternsSet)
    print("Generating done")
    #print(frequentAuthorSet)
    
    print("Generating list allAdvisors of authors from frequentAuthorSet with all associated advisors")
    allAdvisors = patternEvaluation.alladvisors(frequentAuthorSet, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures)
    print("Generating done")
    #print(allAdvisors)
    # Writes advisoradviseerelationshipsevaluation.txt file to predict advisor and advisee relationships and the approximate period for such advisory supervision
    patternEvaluation.evaluateadvisoradviseerelationships(allAdvisors, authorsName, patternEvaluationMeasures, startYear, endYear)