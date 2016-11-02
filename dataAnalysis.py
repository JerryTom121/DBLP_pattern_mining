import matplotlib.pyplot as plt


# Generates dictionaries from source:
# - with the years for keys and the associated number of treatises published
# - with the numbers of coauthors for keys and the associated number of treatises written
def analysis(source):
    
    years = { }
    coauthorscounts = { }

    dblpextract = open(source, "r", encoding = "utf8")
    
    for line in dblpextract:
        list = line.strip().split("\t")
        numberofauthors = len(list) - 2
        if list[len(list) - 1] not in years:
            years[list[len(list) - 1]] = 1
        else:
            years[list[len(list) - 1]] += 1
        if numberofauthors not in coauthorscounts:
            coauthorscounts[numberofauthors] = 1
        else:
            coauthorscounts[numberofauthors] += 1

    dblpextract.close()
    
    return(years, coauthorscounts)


# Plots the number of treatises published per year
def plottreatisesperyear(years):
    
    x = [year for year, count in sorted(years.items(), key = lambda tuple: tuple[0])]
    y = [count for year, count in sorted(years.items(), key = lambda tuple: tuple[0])]
    plt.plot(x, y)
    plt.xlabel("Year")
    plt.ylabel("Number of treatises published")


# Plots the number of treatises per number of coauthors
def plottreatisespercoauthorscount(coauthorscounts):
    
    x = [coauthorscount for coauthorscount, count in sorted(coauthorscounts.items(), key = lambda tuple: tuple[0])]
    y = [count for coauthorscount, count in sorted(coauthorscounts.items(), key = lambda tuple: tuple[0])]
    plt.plot(x, y)
    plt.xlabel("Coauthors count")
    plt.ylabel("Number of treatises")
    

if __name__ == "__main__":

    years, coauthorscounts = analysis("dblpextract.txt")
    
    # Plotting the number of treatises published per year
    plt.figure("Number of treatises published per year")
    plottreatisesperyear(years)
    # Plotting the number of treatises per number of coauthors
    plt.figure("Number of treatises per number of coauthors")
    plottreatisespercoauthorscount(coauthorscounts)