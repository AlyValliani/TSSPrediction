'''
parse.py - Parses the RNA data
Aly Valliani and Michael Superdock
11/15/14
'''

def parse(filename):
    
    myFile = open(filename, 'r')

    dictionary = {}
    while True:
        text = myFile.readline().rstrip() #read line and strip end characters
        if text == "":
            break

        if text[0] == '>':
            tagLine = text.split('|')
            ID = tagLine[0][1:]
            aminoAcid = tagLine[3]
            RNAseq = myFile.readline().rstrip()
            structure = myFile.readline().rstrip()

            RNAseqBases = sorted([x.lower() for x in set(RNAseq)])
            if RNAseqBases == ['a','c','g','t']:
                dictionary[ID] = dict()
                dictionary[ID]["aminoAcid"] = aminoAcid
                dictionary[ID]["sequence"] = sequenceToLower(RNAseq)
                dictionary[ID]["structure"] = structure

    myFile.close()
    return dictionary #a list of feature, classification tuples

def sequenceToLower(RNAseq):
    
    lowerList = ""
    for base in RNAseq:
        lowerList += base.lower()
    return lowerList

def getCounts(dataDict):

    IDs = dataDict.keys()
    stemDict = {}
    loopDict = {}
    pairDict = {}
    baseList = ['a','g','t','c']

    for b in baseList:
        stemDict[b] = 0
        loopDict[b] = 0
        pairDict[b] = dict()
        for b2 in baseList:
            pairDict[b][b2] = 0

    for ID in IDs:
        seq = dataDict[ID]["sequence"]
        struct = dataDict[ID]["structure"]
        for i in range(len(seq)):
            base = seq[i].lower()
            if struct[i] == '(' or struct[i] == ')':
                stemDict[base] += 1
            else:
                loopDict[base] += 1
        
        lst = []
        for i in range(len(struct)):
            if struct[i] == '(':
                lst.append(seq[i].lower())
            elif struct[i] == ')':
                item1 = lst.pop()
                item2 = seq[i].lower()
                pairDict[item1][item2] += 1

    return stemDict, loopDict, pairDict

def outputData(stemDict, loopDict, pairDict):

    baseList = ['a','g','t','c']
    loopTotal = sum(loopDict.values())
    stemTotal = sum(stemDict.values())
    print "\nLoop Percentages:"
    print "Total:", float(loopTotal)/(loopTotal+stemTotal) * 100, "%"
    for b in baseList:
        print b.upper() + ":", float(loopDict[b])/loopTotal * 100, "%"
    print "\nStem Percentages:"
    print "Total:", float(stemTotal)/(loopTotal+stemTotal) * 100, "%"
    for b in baseList:
        print b.upper() + ":", float(stemDict[b])/stemTotal * 100, "%"
    
    print "\nStem Pairings:"
    for i in range(len(baseList)):
        for j in range(i,(len(baseList))):
            b1 = baseList[i]
            b2 = baseList[j]
            if b1 == b2:
                if pairDict[b1][b2] != 0:
                    print b1.upper()+b2.upper()+":", float(pairDict[b1][b2])/(stemTotal/2)*100, "%"
            else:
                pairTotal = float(pairDict[b1][b2] + pairDict[b2][b1])
                if pairTotal != 0:
                    print b1.upper()+b2.upper()+"/"+b2.upper()+b1.upper()+":", pairTotal/(stemTotal/2)*100, "%"

def main():
    dataDict = parse('data.txt')
    stemDict, loopDict, pairDict = getCounts(dataDict)
    outputData(stemDict, loopDict, pairDict)

if __name__ == "__main__":
    main()

