def getTerminals():
    file = open("first_follow2.txt", 'r')
    file.readline()
    file.readline()

    myset = set()
    for line in file:
        line = line.split("|")
        
        if len(line) > 1:
            followTerminals = line[2]
            firstTerminals = line[1]
            for k in " \"\t}{\\":
                firstTerminals = firstTerminals.replace(k, "")
            
            firstTerminals = firstTerminals.split(",")
            for j in firstTerminals:
                myset.add(j)

            for k in " \"\t}{\\":
                followTerminals = followTerminals.replace(k, "")
    
            followTerminals = followTerminals.split(",")
            for j in followTerminals:
                myset.add(j)            

    lst = list(myset)
    lst.append(",")
    refinedList = []
    for j in lst:
        j = j.strip()
        if j and not j in refinedList:
            refinedList.append(j)
    print("Terminals:\n")
    for terminals in refinedList:
        print(terminals)
    return refinedList

getTerminals()
