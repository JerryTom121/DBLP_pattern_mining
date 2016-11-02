import frequentPatternTreeStructure


# Generates a dictionary from source with transactions corresponding to related coauthors' IDs for keys and the associated number of occurrence and years of publication
def database(source):
    
    database = { }
    
    dblpcoauthorsinfo = open(source, "r", encoding = "utf8")
    
    for line in dblpcoauthorsinfo:
        
        list = line.strip().split("\t")
        transaction = [ ]
        
        for index in range(3, len(list)):
            transaction.append(int(list[index]))
                    
        if len(transaction) > 0:
            if frozenset(transaction) not in database:
                database[frozenset(transaction)] = [1, [int(list[1])]]
            else:
                database[frozenset(transaction)][0] += 1
                database[frozenset(transaction)][1].append(int(list[1]))
            
    dblpcoauthorsinfo.close()
    
    return(database)


# Generates a dictionary from data with the authors' IDs for keys and the associated numbers of occurrence in data
def itemsoccurrence(data):
    
    itemsOccurrence = { }
    
    for transaction in data:
        occurrence = data[transaction][0]
        for item in transaction:
            if item not in itemsOccurrence:
                itemsOccurrence[item] = occurrence
            else:
                itemsOccurrence[item] += occurrence
    
    return(itemsOccurrence)

# Generates a dictionary from itemsOccurrence for items with support count superior or equal to minSupportCount
def frequentitems(itemsOccurence, minSupportCount):
    
    return({item: supportCount for item, supportCount in itemsOccurence.items() if supportCount >= minSupportCount})


# Generates a dictionary from data for transaction with frequent items only
def dataset(data, frequentItems):

    dataSet = { }

    for transaction, information in data.items():
        occurrence = information[0]
        updatedTransaction = [ ]
        for item in transaction:
            if item in frequentItems:
                updatedTransaction.append(item)
        if len(updatedTransaction) > 0:
            if frozenset(updatedTransaction) not in dataSet:
                dataSet[frozenset(updatedTransaction)] = [occurrence, information[1]]
            else:
                dataSet[frozenset(updatedTransaction)][0] += occurrence
                if information[1] != None:
                    dataSet[frozenset(updatedTransaction)][1] += information[1]
    
    return(dataSet)


# Generates a FP-tree and its items-header table from dataSet and frequentItems   
def createFPtree(dataSet, frequentItems):
    
    FPTree = frequentPatternTreeStructure.FPTree(frequentItems)
    
    if len(frequentItems) == 0:
        return(None)
    else:
        for transaction in dataSet:
            unsortedTransaction = [ ]
            for item in transaction:
                unsortedTransaction.append(item)
            count = dataSet[transaction][0]
            sortedTransaction = sorted(unsortedTransaction, key = lambda x: frequentItems[x], reverse = True)
            FPTree.inserttransaction(sortedTransaction, FPTree.gettree(), count)
        return(FPTree)


# Adds frequentPattern into frequentPatternSet with count as the number of occurrence
def addfrequentpattern(frequentPattern, frequentPatternSet, count = 1):

    if frozenset(frequentPattern) not in frequentPatternSet:
        frequentPatternSet[frozenset(frequentPattern)] = count
    else:
        frequentPatternSet[frozenset(frequentPattern)] += count


# Mines FPTree and saves the frequent patterns into frequentPatternSet
def mineFPtree(FPTree, frequentItemSet, frequentPatternSet, minSupportCount):
        
    headerTable = FPTree.getheadertable()
    sortedHeader = [item[0] for item in sorted(headerTable.items(), key = lambda tuple: tuple[1][0])]
    
    for item in sortedHeader:
        
        newFrequentItemsSet = frequentItemSet.copy()
        newFrequentItemsSet.add(item)
        
        if len(newFrequentItemsSet) > 1:
            addfrequentpattern(newFrequentItemsSet, frequentPatternSet, headerTable[item][0])

        prefixPaths = FPTree.conditionalpatternbase(headerTable[item][1])
        conditionalFrequentItems = frequentitems(itemsoccurrence(prefixPaths), minSupportCount)
        conditionalDataSet = dataset(prefixPaths, conditionalFrequentItems)
        conditionalFPTree = createFPtree(conditionalDataSet, conditionalFrequentItems)
        
        if conditionalFPTree != None:
            mineFPtree(conditionalFPTree, newFrequentItemsSet, frequentPatternSet, minSupportCount)
