import xml.sax as XML


class DblpContentHandler(XML.ContentHandler):
    
    def __init__(self, keyWord):
        
        self.depth = 0
        self.current = ""
        self.content = ""
        self.data = {"title": [], "author": [], "year": []}
        self.keyWord = keyWord

    def startElement(self, name, attrs):
        
        self.depth += 1
        self.current = name
        
        if self.depth == 2:
            self.data = {"title": [], "author": [], "year": []}
            
        if self.depth >= 3:
            self.content = ""

    def endElement(self, name):
        
        if self.depth == 2:
            line = ""
            authorsCount = 0
            authorsNames = ""
            date = ""
            for title in self.data["title"]:
                line += title
            for author in self.data["author"]:
                authorsCount += 1
                authorsNames += "\t" + author
            for year in self.data["year"]:
                date = year
            if self.keyWord in line and authorsCount >= 1:
                line += authorsNames + "\t" + date + "\n"
                dblpextract.write(line.encode("utf8"))
            
        if self.depth >= 3:
            if name in self.data:
                self.data[name].append(self.content)
            
        self.depth -= 1

    def characters(self, content):
        
        if content != '\n':
            self.content += content        


# Writes a .txt file from source with only treatises' title, authors' names and date of publication seperated by \t for treatises including keyWord in the title
def createfiledblpextract(source, keyWord):

    handler = DblpContentHandler(keyWord)
    XML.parse(source, handler)
    
    
if __name__ == "__main__":
    
    keyWord = "Data"
    
    # Writes a .txt file from dblp.xml with only treatises' title, authors' names and date of publication seperated by \t for treatises including keyWord in the title
    # dblpextract.txt file structure: Title\tAuthor...\n
    print("Writing a .txt file from dblp.xml with only treatises' title, authors' names and date of publication seperated by '\t' for treatises including " + keyWord + " in the title")
    dblpextract = open("dblpextract.txt", "wb")
    createfiledblpextract("dblp.xml", keyWord)
    dblpextract.close()
    print("Writing dblpextract.txt done")
