import math
import random
import pandas
import csv


class PatternEvaluationMeasures():

    def __init__(self, dataSet):
        self.dataSet = dataSet
        self.N = 0
        for transaction in dataSet:
            self.N += dataSet[transaction][0]

    def getdataset(self):
        return self.dataSet
    
    def getN(self):
        return self.N
    
    # Counts the number of transations that contain itemSetX in dataSet
    def supportcountX(self, itemSetX, startYear, endYear):
        count = 0
        for transaction in self.dataSet:
            if frozenset(itemSetX) <= transaction:
                count += len([year for year in self.dataSet[transaction][1] if startYear <= year and year <= endYear])
        return count

    # Counts the number of transations that contain both itemSetX and itemSetY in dataSet
    def supportcountXY(self, itemSetX, itemSetY, startYear, endYear):
        count = 0
        for transaction in self.dataSet:
            if (frozenset(itemSetX) <= transaction) and (frozenset(itemSetY) <= transaction):
                count += len([year for year in self.dataSet[transaction][1] if startYear <= year and year <= endYear])
        return count
    
    # Counts the number of transations that contain itemSetX and not itemSetY in dataSet
    def supportcountXnonY(self, itemSetX, itemSetY, startYear, endYear):
        count = 0
        for transaction in self.dataSet:
            if (frozenset(itemSetX) <= transaction) and not (frozenset(itemSetY) <= transaction):
                count += len([year for year in self.dataSet[transaction][1] if startYear <= year and year <= endYear])
        return count

    # Counts the number of transations that contain nor itemSetX and neither itemSetY in dataSet
    def supportcountnonXnonY(self, itemSetX, itemSetY, startYear, endYear):
        count = 0
        for transaction in self.dataSet:
            if not (frozenset(itemSetX) <= transaction) and not (frozenset(itemSetY) <= transaction):
                count += len([year for year in self.dataSet[transaction][1] if startYear <= year and year <= endYear])
        return count
    
    # Computes relevant supports count for association rule (itemSetX -> itemSetY)
    def computesupportcount(self, itemSetX, itemSetY, startYear, endYear):
        supportXY = self.supportcountXY(itemSetX, itemSetY, startYear, endYear)
        supportXnonY = self.supportcountXnonY(itemSetX, itemSetY, startYear, endYear)
        supportnonXY = self.supportcountXnonY(itemSetY, itemSetX, startYear, endYear)
        supportnonXnonY = self.supportcountnonXnonY(itemSetX, itemSetY, startYear, endYear)
        supportX = supportXY + supportXnonY
        supportY = supportXY + supportnonXY
        supportnonX = supportnonXY + supportnonXnonY
        supportnonY = supportXnonY + supportnonXnonY

        return supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY

    def correlation(self, supportXY, supportX, supportY, supportnonX, supportnonY):
        return (self.N * supportXY - supportX * supportY) / math.sqrt(supportX * supportY * supportnonX * supportnonY)
    
    def kappa(self, supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY):
        return (self.N * supportXY + self.N * supportnonXnonY - supportX * supportY - supportnonX * supportnonY) / (self.N**2 - supportX * supportY - supportnonX * supportnonY)

    def certaintyfactor(self, supportXY, supportX, supportY):
        return max(((supportXY / supportX) - (supportY / self.N)) / (1 - (supportY / self.N)), ((supportXY / supportY) - (supportX / self.N)) / (1 - (supportX / self.N)))

    def addedvalue(self, supportXY, supportX, supportY):
        return max((supportXY / supportX) - (supportY / self.N), (supportXY / supportY) - (supportX / self.N))

    def piatetskyshapiro(self, supportXY, supportX, supportY):        
        return (supportXY / self.N) - (supportX * supportY) / self.N**2

    def jmeasure(self, supportXY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY):
        if supportXnonY == 0 or supportnonXY == 0:
            return float('NaN')
        else:
            return ((supportXY / self.N) * math.log(self.N * supportXY / (supportX * supportY))) + max((supportXnonY / self.N) * math.log(self.N * supportXnonY / (supportX * supportnonY)), (supportnonXY / self.N) * math.log(self.N * supportnonXY / (supportnonX * supportY)))

    def giniindex(self, supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY):
        return max((supportX / self.N) * ((supportXY / supportX)**2 + (supportXnonY / supportX)**2) + (supportnonX / self.N) * ((supportnonXY / supportnonX)**2 + (supportnonXnonY / supportnonX)**2) - (supportY / self.N)**2 - (supportnonY / self.N)**2, (supportY / self.N) * ((supportXY / supportY)**2 + (supportnonXY / supportY)**2) + (supportnonY / self.N) * ((supportXnonY / supportnonY)**2 + (supportnonXnonY / supportnonY)**2) - (supportX / self.N)**2 - (supportnonX / self.N)**2)

    # Counts proportion of transactions that contain itemSetY among the transactions that contain itemSetX
    def confidenceXY(self, supportXY, supportX):
        return supportXY / supportX

    # Counts proportion of transactions that contain itemSetX among the transactions that contain itemSetY        
    def confidenceYX(self, supportXY, supportY):
        return supportXY / supportY   
        
    def maxConfidence(self, supportXY, supportX, supportY):
        return max(supportXY / supportX, supportXY / supportY)
    
    def allConfidence(self, supportXY, supportX, supportY):
        return supportXY / max(supportX, supportY)

    def laplace(self, supportXY, supportX, supportY):
        return max((supportXY + 1) / (supportX + 2), (supportXY + 1) / (supportY + 2))        

    def cosine(self, supportXY, supportX, supportY):
        return supportXY / math.sqrt(supportX * supportY)

    def coherence(self, supportXY, supportX, supportY):
        return supportXY / (supportX + supportY - supportXY)
        
    def kulc(self, supportXY, supportX, supportY):
        return supportXY * (1 / supportX + 1 / supportY) / 2
    
    def oddsratio(self, supportXY, supportnonXnonY, supportXnonY, supportnonXY):        
        if supportXnonY * supportnonXY == 0:
            return float('NaN')
        else:
            return (supportXY * supportnonXnonY) / (supportXnonY * supportnonXY)

    def lift(self, supportXY, supportX, supportY):
        return (self.N * supportXY) / (supportX * supportY)

    def collectivestrength(self, supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY):        
        if supportX * supportY + supportnonX * supportnonY == 0 or self.N - supportXY - supportnonXnonY ==0:
            return float('NaN')
        else:
            return ((supportXY + supportnonXnonY) / (supportX * supportY + supportnonX * supportnonY)) * ((self.N**2 - supportX * supportY - supportnonX * supportnonY) / (self.N - supportXY - supportnonXnonY))

    def conviction(self, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY):
        if supportXnonY == 0 or supportXnonY == 0:
            return float('NaN')
        else:
            return max((supportX * supportnonY) / (self.N * supportXnonY), (supportnonX * supportY) / (self.N * supportXnonY))
    
    def imbalanceratio(self, supportX, supportY, supportXY):
        return math.fabs(supportX - supportY) / (supportX + supportY - supportXY)


# Generates a dictionary from frequentPatternSet for patterns of length equal to 2
def evaluatedfrequentpatternsset(frequentPatternSet):

    return({pattern: supportCount for pattern, supportCount in frequentPatternSet.items() if len(pattern) == 2})


# Generates a sample of size k from evaluatedFrequentPatternsSet
def frequentpatternssetsample(evaluatedFrequentPatternsSet, k):

    return(random.sample(evaluatedFrequentPatternsSet.items(), k))

    
def removeduplicates(list):

    modifiedlist = [ ]
    for item in list:
        if item not in modifiedlist:
            modifiedlist.append(item)
    return(modifiedlist)


def findindices(list, item):

    return([i for i, x in enumerate(list) if x == item])

# Writes .cvs files with frequentPatternSetSample evaluated and ranked by interestingness measures  
def rankfrequentpatternssamplemeasures(frequentPatternSetSample, k, authorsName, startYear, endYear, patternEvaluationMeasures):

    print("Writing .csv files with frequentPatternSetSample evaluated and ranked by interestingness measures")

    measures = {"Author X & Author Y": [ ], "Correlation": [ ], "Kappa": [ ], "Certainty Factor": [ ], "Added Value": [ ], "Piatetsky Shapiro": [ ], "J-Measure": [ ], "Gini Index": [ ], "MaxConfidence": [ ], "AllConfidence": [ ], "Laplace": [ ], "Cosine": [ ], "Coherence": [ ], "Kulc": [ ], "Odds Ratio": [ ], "Lift": [ ], "Collective Strength": [ ], "Conviction": [ ], "Imbalance Ratio": [ ]}
    
    rankings = {"Author X & Author Y": [ ], "Correlation": [0] * k, "Kappa": [0] * k, "Certainty Factor": [0] * k, "Added Value": [0] * k, "Piatetsky Shapiro": [0] * k, "J-Measure": [0] * k, "Gini Index": [0] * k, "MaxConfidence": [0] * k, "AllConfidence": [0] * k, "Laplace": [0] * k, "Cosine": [0] * k, "Coherence": [0] * k, "Kulc": [0] * k, "Odds Ratio": [0] * k, "Lift": [0] * k, "Collective Strength": [0] * k, "Conviction": [0] * k, "Imbalance Ratio": [0] * k}
    
    for pattern, support in frequentPatternSetSample:
        
        patternList = list(pattern)
        authorX = patternList[0]
        authorY = patternList[1]
        
        supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY = patternEvaluationMeasures.computesupportcount([authorX], [authorY], startYear, endYear)

        measures["Author X & Author Y"].append(authorsName[authorX][0] + " & " + authorsName[authorY][0])
        measures["Correlation"].append(patternEvaluationMeasures.correlation(supportXY, supportX, supportY, supportnonX, supportnonY))
        measures["Kappa"].append(patternEvaluationMeasures.kappa(supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY))
        measures["Certainty Factor"].append(patternEvaluationMeasures.certaintyfactor(supportXY, supportX, supportY))
        measures["Added Value"].append(patternEvaluationMeasures.addedvalue(supportXY, supportX, supportY))
        measures["Piatetsky Shapiro"].append(patternEvaluationMeasures.piatetskyshapiro(supportXY, supportX, supportY))
        measures["J-Measure"].append(patternEvaluationMeasures.jmeasure(supportXY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY))
        measures["Gini Index"].append(patternEvaluationMeasures.giniindex(supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY))
        measures["MaxConfidence"].append(patternEvaluationMeasures.maxConfidence(supportXY, supportX, supportY))
        measures["AllConfidence"].append(patternEvaluationMeasures.allConfidence(supportXY, supportX, supportY))
        measures["Laplace"].append(patternEvaluationMeasures.laplace(supportXY, supportX, supportY))
        measures["Cosine"].append(patternEvaluationMeasures.cosine(supportXY, supportX, supportY))
        measures["Coherence"].append(patternEvaluationMeasures.coherence(supportXY, supportX, supportY))
        measures["Kulc"].append(patternEvaluationMeasures.kulc(supportXY, supportX, supportY))
        measures["Odds Ratio"].append(patternEvaluationMeasures.oddsratio(supportXY, supportnonXnonY, supportXnonY, supportnonXY))
        measures["Lift"].append(patternEvaluationMeasures.lift(supportXY, supportX, supportY))
        measures["Collective Strength"].append(patternEvaluationMeasures.collectivestrength(supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY))
        measures["Conviction"].append(patternEvaluationMeasures.conviction(supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY))
        measures["Imbalance Ratio"].append(patternEvaluationMeasures.imbalanceratio(supportX, supportY, supportXY))

    pandas.DataFrame(measures).to_csv('frequentpatternssamplemeasures.csv', index = False)

    rankings["Author X & Author Y"] = measures["Author X & Author Y"]
    rank = 1
    for value in removeduplicates(sorted(measures["Correlation"], reverse = True)):
        count = rank
        for index in findindices(measures["Correlation"], value):
            rankings["Correlation"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Kappa"], reverse = True)):
        count = rank
        for index in findindices(measures["Kappa"], value):
            rankings["Kappa"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Certainty Factor"], reverse = True)):
        count = rank
        for index in findindices(measures["Certainty Factor"], value):
            rankings["Certainty Factor"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Added Value"], reverse = True)):
        count = rank
        for index in findindices(measures["Added Value"], value):
            rankings["Added Value"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Piatetsky Shapiro"], reverse = True)):
        count = rank
        for index in findindices(measures["Piatetsky Shapiro"], value):
            rankings["Piatetsky Shapiro"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["J-Measure"], reverse = True)):
        count = rank
        for index in findindices(measures["J-Measure"], value):
            rankings["J-Measure"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Gini Index"], reverse = True)):
        count = rank
        for index in findindices(measures["Gini Index"], value):
            rankings["Gini Index"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["MaxConfidence"], reverse = True)):
        count = rank
        for index in findindices(measures["MaxConfidence"], value):
            rankings["MaxConfidence"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["AllConfidence"], reverse = True)):
        count = rank
        for index in findindices(measures["AllConfidence"], value):
            rankings["AllConfidence"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Laplace"], reverse = True)):
        count = rank
        for index in findindices(measures["Laplace"], value):
            rankings["Laplace"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Cosine"], reverse = True)):
        count = rank
        for index in findindices(measures["Cosine"], value):
            rankings["Cosine"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Coherence"], reverse = True)):
        count = rank
        for index in findindices(measures["Coherence"], value):
            rankings["Coherence"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Kulc"], reverse = True)):
        count = rank
        for index in findindices(measures["Kulc"], value):
            rankings["Kulc"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Odds Ratio"], reverse = True)):
        count = rank
        for index in findindices(measures["Odds Ratio"], value):
            rankings["Odds Ratio"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Lift"], reverse = True)):
        count = rank
        for index in findindices(measures["Lift"], value):
            rankings["Lift"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Collective Strength"], reverse = True)):
        count = rank
        for index in findindices(measures["Collective Strength"], value):
            rankings["Collective Strength"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Conviction"], reverse = True)):
        count = rank
        for index in findindices(measures["Conviction"], value):
            rankings["Conviction"][index] = count
            rank += 1
    rank = 1
    for value in removeduplicates(sorted(measures["Imbalance Ratio"])):
        count = rank
        for index in findindices(measures["Imbalance Ratio"], value):
            rankings["Imbalance Ratio"][index] = count
            rank += 1

    pandas.DataFrame(rankings).to_csv('frequentpatternssamplerankings.csv', index = False)
    
    print("Writing frequentpatternssamplemeasures.csv and frequentpatternssamplerankings.csv done")


class AuthorAdvisoryRelationship():
    
    def __init__(self, author, advisors = None):
        self.author = author
        self.advisors = advisors

    def getauthor(self):
        return self.author
    
    def getadvisors(self):
        return self.advisors
    
    def getadvisoryperiod(self, advisor):
        if advisor in self.getadvisors():
            return self.advisors[advisor]
        else:
            return None
    
    def addadvisor(self, advisor, advisoryPeriod):
        if self.getadvisors() == None:
            self.advisors = {advisor: advisoryPeriod}
        else:
            if advisor not in self.getadvisors():
                self.advisors[advisor] = advisoryPeriod
    
    def removeadvisor(self, advisor):
        if advisor in self.getadvisors():
            if len(self.getadvisors()) == 1:
                self.advisors = None
            else:
                del(self.advisors[advisor])


# Generates a sample of size k of authors from evaluatedFrequentPatternsSet
def frequentauthorsset(evaluatedFrequentPatternsSet):
    
    frequentAuthorSet = set([ ])
    for frequentPatternSet in evaluatedFrequentPatternsSet.keys():
        frequentAuthorSet = frequentAuthorSet | frequentPatternSet - frequentAuthorSet | frequentPatternSet
    
    return(frequentAuthorSet)


def advisoradviseerelationshipispossible(advisor, advisee, authorsName, startPeriod, endPeriod, patternEvaluationMeasures):
    
    year = startPeriod
    supportX = patternEvaluationMeasures.supportcountX([advisor], startPeriod, year)
    supportY = patternEvaluationMeasures.supportcountX([advisee], startPeriod, year)
    supportXY = patternEvaluationMeasures.supportcountXY([advisor], [advisee], startPeriod, year)
    kulc = (supportXY / 2) * (1 / supportX + 1 / supportY)
    sequenceimbalanceratioispositive = ((supportX - supportY) / (supportX + supportY - supportXY)) >= 0
    sequencekulcincreases = True

    while sequenceimbalanceratioispositive and sequencekulcincreases and year + 1 <= endPeriod:
        year += 1
        supportX = patternEvaluationMeasures.supportcountX([advisor], startPeriod, year)
        supportY = patternEvaluationMeasures.supportcountX([advisee], startPeriod, year)
        supportXY = patternEvaluationMeasures.supportcountXY([advisor], [advisee], startPeriod, year)
        nextkulc = (supportXY / 2) * (1 / supportX + 1 / supportY)
        sequenceimbalanceratioispositive = ((supportX - supportY) / (supportX + supportY - supportXY)) >= 0
        sequencekulcincreases = nextkulc >= kulc
        kulc = nextkulc
    
    return(authorsName[advisor][1][0] < authorsName[advisee][1][0] and endPeriod - startPeriod > 1 and authorsName[advisor][1][0] + 2 <= startPeriod and sequenceimbalanceratioispositive and sequencekulcincreases)


def estimatedstartperiod(advisor, advisee, patternEvaluationMeasures):

    dataSet = patternEvaluationMeasures.getdataset()
    collaborationyears = [ ]
    
    for transaction in dataSet:
        if (frozenset([advisor]) <= transaction) and (frozenset([advisee]) <= transaction):
            collaborationyears += dataSet[transaction][1]
    
    return(min(collaborationyears))


def estimatedendperiod(advisor, advisee, startPeriod, endYear, patternEvaluationMeasures):

    year = startPeriod
    supportX = patternEvaluationMeasures.supportcountX([advisor], startPeriod, year)
    supportY = patternEvaluationMeasures.supportcountX([advisee], startPeriod, year)
    supportXY = patternEvaluationMeasures.supportcountXY([advisor], [advisee], startPeriod, year)
    kulc = (supportXY / 2) * (1 / supportX + 1 / supportY)

    while year < endYear:
        supportX = patternEvaluationMeasures.supportcountX([advisor], startPeriod, year + 1)
        supportY = patternEvaluationMeasures.supportcountX([advisee], startPeriod, year + 1)
        supportXY = patternEvaluationMeasures.supportcountXY([advisor], [advisee], startPeriod, year + 1)
        nextkulc = (supportXY / 2) * (1 / supportX + 1 / supportY)
        if nextkulc >= kulc:
            year += 1
            kulc = nextkulc
        else:
            break

    return(year)


def potentialadvisors(author, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures):
    
    potentialAdvisors = AuthorAdvisoryRelationship(author)
    
    for pattern in evaluatedFrequentPatternsSet.keys():
        if author in pattern:
            patternList = list(pattern)
            if author == patternList[0]:
                coauthor = patternList[1]
            else:
                coauthor = patternList[0]
            startPeriod = estimatedstartperiod(coauthor, author, patternEvaluationMeasures)
            endPeriod = estimatedendperiod(coauthor, author, startPeriod, endYear, patternEvaluationMeasures)
            if advisoradviseerelationshipispossible(coauthor, author, authorsName, startPeriod, endPeriod, patternEvaluationMeasures):
                potentialAdvisors.addadvisor(coauthor, [startPeriod, endPeriod])

    return(potentialAdvisors)


def allpotentialadvisors(frequentAuthorSet, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures):
    
    allPotentialAdvisors = [potentialadvisors(author, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures) for author in frequentAuthorSet]
    
    return([potentialAdvisors for potentialAdvisors in allPotentialAdvisors  if potentialAdvisors.getadvisors() != None])


def authorpotentialadvisors(author, allPotentialAdvisors):
    
    for authorPotentialAdvisors in allPotentialAdvisors:
       if  authorPotentialAdvisors.getauthor() == author:
           return(authorPotentialAdvisors)
           break
    
    return(None)


# Generates a list of authors from frequentAuthorSet with all associated advisors
def alladvisors(frequentAuthorSet, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures):
        
    allPotentialAdvisors = allpotentialadvisors(frequentAuthorSet, authorsName, evaluatedFrequentPatternsSet, endYear, patternEvaluationMeasures)
    excludedAdvisors = { }
    
    for authorAdvisoryRelationship in allPotentialAdvisors:
        if authorAdvisoryRelationship.getadvisors() != None:
            for advisor in authorAdvisoryRelationship.getadvisors():
                advisorPotentialAdvisors = authorpotentialadvisors(advisor, allPotentialAdvisors)
                if advisorPotentialAdvisors != None:
                    if advisorPotentialAdvisors.getadvisors() != None:
                        for advisorsadvisor in advisorPotentialAdvisors.getadvisors():
                            timeline = advisorPotentialAdvisors.getadvisoryperiod(advisorsadvisor) + authorAdvisoryRelationship.getadvisoryperiod(advisor)
                            if timeline != sorted(timeline):
                                excludedAdvisors[advisorPotentialAdvisors.getauthor()] = advisorsadvisor
                                excludedAdvisors[authorAdvisoryRelationship.getauthor()] = advisor
    
    for authorAdvisoryRelationship in allPotentialAdvisors:
        if authorAdvisoryRelationship.getauthor() in excludedAdvisors:
            authorAdvisoryRelationship.removeadvisor(excludedAdvisors[authorAdvisoryRelationship.getauthor()])
    
    return([potentialAdvisors for potentialAdvisors in allPotentialAdvisors if potentialAdvisors.getadvisors() != None])
       

# Writes a .csv file to predict advisor and advisee relationships and the approximate period for such advisory supervision
def evaluateadvisoradviseerelationships(allAdvisors, authorsName, patternEvaluationMeasures, startYear, endYear):

    print("Writing a .csv file to predict advisor and advisee relationships and the approximate period for such advisory supervision")
    advisoradviseerelationshipsevaluation = open("advisoradviseerelationshipsevaluation.csv", "w")
    
    csvwriter = csv.writer(advisoradviseerelationshipsevaluation)
    csvwriter.writerow(['Advisor X', 'Advisee Y', 'StartPeriod', 'EndPeriod', 'Support(X,Y)', 'Support(X)', 'Support(Y)', 'Confidence(X->Y)', 'Confidence(Y->X)', 'StartYear', 'EndYear', 'Support(X,Y)', 'Support(X)', 'Support(Y)', 'Confidence(X->Y)', 'Confidence(Y->X)'])

    for authorAdvisoryRelationship in allAdvisors:
        
        advisee = authorAdvisoryRelationship.getauthor()
        
        for advisor in authorAdvisoryRelationship.getadvisors():
        
            period = authorAdvisoryRelationship.getadvisoryperiod(advisor)
            supportXY, supportnonXnonY, supportX, supportY, supportnonX, supportnonY, supportXnonY, supportnonXY = patternEvaluationMeasures.computesupportcount(set([advisor]), set([advisee]), period[0], period[1])
            totalSupportXY, totalSupportnonXnonY, totalSupportX, totalSupportY, totalSupporttnonX, totalSupportnonY, totalSupportXnonY, totalSupportnonXY = patternEvaluationMeasures.computesupportcount(set([advisor]), set([advisee]), startYear, endYear)
    
            csvwriter.writerow([authorsName[advisor][0], authorsName[advisee][0], period[0], period[1], supportXY, supportX, supportY, patternEvaluationMeasures.confidenceXY(supportXY, supportX), patternEvaluationMeasures.confidenceYX(supportXY, supportY), startYear, endYear, totalSupportXY, totalSupportX, totalSupportY, patternEvaluationMeasures.confidenceXY(totalSupportXY, totalSupportX), patternEvaluationMeasures.confidenceYX(totalSupportXY, totalSupportY)])
    
    advisoradviseerelationshipsevaluation.close()
    print("Writing advisoradviseerelationshipsevaluation.csv done")