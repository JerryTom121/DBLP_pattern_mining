# Writes a .txt file from source with the author's ID, name, number of occurrence and years of publication in source seperated by \t
def createfileauthors(source):
    
    print("Writing a .txt file from " + str(source) + " with the author's ID, name, number of occurrence and years of publication in source seperated by '\t'")
    dblpauthorsinfo = open("dblpauthorsinfo.txt", "w")

    authors = { }

    dblpextract = open(source, "r", encoding = "utf8")
    
    for line in dblpextract:
        list = line.strip().split("\t")
        for i in range(1, len(list) - 1):
            if list[i] not in authors:
                authors[list[i]] = [1, [int(list[len(list) - 1])]]
            else:
                authors[list[i]][0] += 1
                authors[list[i]][1].append(int(list[len(list) - 1]))

    dblpextract.close()
    
    index = 0
    for author in sorted(authors.keys()):
        index = index + 1
        line = str(index) + "\t" + str(author) + "\t" + str(authors[author][0])
        for year in authors[author][1]:
            line += "\t" + str(year)
        line += "\n"
        dblpauthorsinfo.write(line)

    dblpauthorsinfo.close()
    print("Writing dblpauthorsinfo.txt done")


# Generates a dictionary from source with the authors' names for keys and the associated IDs and years of publication in chronological order
def authorsid(source):
    
    authorsID = { }
    
    dblpauthorsinfo = open(source, "r")

    for line in dblpauthorsinfo:
        list = line.strip().split("\t")
        authorsID[list[1]] = [int(list[0]), sorted([int(year) for year in list[3:len(list)]])]

    dblpauthorsinfo.close()
    
    return(authorsID)

# Generates a dictionary from authorsID with the authors' IDs for keys and the associated names and years of publication in chronological order
def authorsname(authorsID):
    
    return({information[0]: [name, information[1]] for name, information in authorsID.items()})


# Writes a .txt file from source with treatises' title's IDs, year of publication, number of authors and authors' IDs seperated by \t
def createfilecoauthors(source, authorsID):
    
    print("Writing a .txt file from " + str(source) + " with treatises' title's IDs, year of publication, number of authors and authors' IDs seperated by '\t'")
    dblpcoauthorsinfo = open("dblpcoauthorsinfo.txt", "w")
    
    dblpextract = open(source, "r", encoding = "utf8")

    startYear = 10000
    endYear = 0

    count = 0
    for line in dblpextract:
        count += 1
        list = line.strip().split("\t")
        if int(list[len(list)-1]) < startYear:
            startYear = int(list[len(list)-1])
        if int(list[len(list)-1]) > endYear:
            endYear = int(list[len(list)-1])
        info = str(count) + "\t" + list[len(list)-1] + "\t" + str(len(list) - 2)
        for i in range(1, len(list) - 1):
            if list[i] in authorsID:
                info += "\t" + str(authorsID[list[i]][0])
        info += "\n"
        dblpcoauthorsinfo.write(info)

    dblpextract.close()
    
    dblpcoauthorsinfo.close()
    print("Writing dblpcoauthorsinfo.txt done")
    
    return(startYear, endYear)