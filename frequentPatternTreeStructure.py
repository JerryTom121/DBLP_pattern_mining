class FPNode():
    
    def __init__(self, item, weight = 0, depth = 0, parentNode = None):
        self.item = item
        self.weight = weight
        self.depth = depth
        self.parent = parentNode
        self.children = { }
        self.nodeLink = None

    def getitem(self):
        return self.item
    
    def getweight(self):
        return self.weight

    def incrweight(self, count = 1):
        self.weight += count
    
    def getdepth(self):
        return self.depth
    
    def getparent(self):
        return self.parent
    
    def getchildren(self):
        return self.children.values()
    
    def haschild(self, item):
        return item in self.children
    
    def getchild(self, item):
        if self.haschild(item):
            return self.children[item]
        else:
            return None
    
    def addchild(self, item, count = 1):
        if self.haschild(item):
            self.getchild[item].incrweight(count)
        else:
            self.children[item] = FPNode(item, count, self.getdepth() + 1, self)        

    def getnodelink(self):
        return self.nodeLink

    def printtree(self, file):
        
        node = ""        
        for i in range(1, self.getdepth() + 1):
            node += "\t"
        node += "Depth: " + str(self.getdepth()) + " | Item: " + str(self.getitem()) + ", weight: " + str(self.getweight())        
        file.write(node + "\n")

        for child in self.getchildren():
            child.printtree(file)


class FPTree():
    
    def __init__(self, frequentItems, root = "Null"):
        self.headerTable = { }
        for item in frequentItems:
            self.headerTable[item] = [frequentItems[item], None]
        self.tree = FPNode(root)
        
    def getheadertable(self):
        return self.headerTable

    def getheadertableitemlink(self, item):
        return self.getheadertable()[item][1]
    
    def createitemlink(self, item, node):
        self.getheadertable()[item][1] = node
    
    def updateitemlink(self, item, node):
        testedNode = self.getheadertableitemlink(item)
        while testedNode.getnodelink() != None:
            testedNode = testedNode.getnodelink()
        testedNode.nodeLink = node

    def gettree(self):
        return self.tree
    
    def printheadertable(self):
        for item in self.headerTable:
            node = self.getheadertableitemlink(item)
            print(item + " points to node of depth " + str(node.getdepth()) + " and weight " + str(node.getweight()) + ", child of node " + node.getparent().getitem())

    def printtree(self):
        print("Writing a .txt file with the FPTree structure")
        FPTree = open("FPTree.txt", "w")
        self.gettree().printtree(FPTree)
        FPTree.close()
        print("Writing FPTree.txt done")
        
    def inserttransaction(self, transaction, tree, count = 1):
                
        if len(transaction) >= 1:
            
            item = transaction.pop(0)
            
            if tree.haschild(item):
                tree.getchild(item).incrweight(count)
                
            else:
                tree.addchild(item, count)
                if self.getheadertableitemlink(item) == None:
                    self.createitemlink(item, tree.getchild(item))
                else:
                    self.updateitemlink(item, tree.getchild(item))
                    
            if len(transaction) != 0:
                self.inserttransaction(transaction, tree.getchild(item), count)
    
    def ascendfromnode(self, node, path):
        
        if node.getparent() != None:
            path.append(node.getitem())
            self.ascendfromnode(node.getparent(), path)

    def conditionalpatternbase(self, node):
        
        prefixPaths = { }
        
        while node != None:
            path = [ ]
            self.ascendfromnode(node, path)
            if len(path) > 1:
                prefixPaths[frozenset(path[1:])] = [node.getweight(), None]
            node = node.getnodelink()
            
        return prefixPaths