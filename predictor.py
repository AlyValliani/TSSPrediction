from parse import parse
from collections import defaultdict

def createProductions():

    productions = {}
    productions['single'] = {}
    productions['double'] = {}
    #productions['single']['S'] = [('a .',0.1),('g .',0.1),('c .',0.1),('t .',0.1)]
    #productions['single']['L'] = [('a .',0.1),('g .',0.1),('c .',0.1),('t .',0.1)]
    #productions['double']['S'] = [('L S', 0.1),('Da Ft',0.1),('Dt Fa', 0.1), ('Dg Ft',0.1), ('Dt Fg', 0.1), ('Dg Fc', 0.05), ('Dc Fg', 0.05)]
    productions['double']['F'] = [('F F', 0.05), ('Da_1 Ft',0.05), ('Dt_1 Fa', 0.05), ('Dg_1 Ft', 0.05), ('Dt_1 Fg', 0.05), ('Dg_1 Fc', 0.05), ('Dc_1 Fg', 0.05)]
    productions['single']['F'] = [('a .',0.2),('g .',0.2),('c .',0.2),('t .',0.05)]

    #productions['double']['L'] = [('Da_1 Ft',0.1), ('Dt_1 Fa',0.1), ('Dg_1 Ft', 0.1), ('Dt_1 Fg', 0.1), ('Dg_1 Fc', 0.1), ('Dc_1 Fg', 0.1)]
    productions['double']['Ft'] = [('F Dt_2',1)]
    productions['double']['Fa'] = [('F Da_2',1)]
    productions['double']['Fg'] = [('F Dg_2',1)]
    productions['double']['Fc'] = [('F Dc_2',1)]
    productions['single']['Da_1'] = [('a (',1)]
    productions['single']['Dg_1'] = [('g (',1)]
    productions['single']['Dt_1'] = [('t (',1)]
    productions['single']['Dc_1'] = [('c (',1)]
    productions['single']['Da_2'] = [('a )',1)]
    productions['single']['Dg_2'] = [('g )',1)]
    productions['single']['Dt_2'] = [('t )',1)]
    productions['single']['Dc_2'] = [('c )',1)]

    return productions

def createProductions2():

    productions = {}
    productions['single'] = {}
    productions['double'] = {}

    productions['double']['F'] = [('F F', 0.3), ('D_1 Fd',0.15), ('F D_2',0.15)]
    productions['single']['F'] = [('a .',0.1),('g .',0.1),('c .',0.1),('t .',0.1)]

    productions['single']['D_1'] = [('a (',0.25), ('g (',0.25), ('c (',0.25), ('t (',0.25)]
    productions['single']['D_2'] = [('a )',0.25), ('g )',0.25), ('c )',0.25), ('t )',0.25)]

    return productions

def insideOutside(grammar, dataDict):
    
    IDs = dataDict.keys()[0:100]
    for i in range(len(IDs)):
        print "%d/%d" % (i, len(IDs))
        ID = IDs[i]
        sequence = dataDict[ID]["sequence"]
        structure = dataDict[ID]["structure"]
        #print sequence
        #print structure
        insideOutsideLoop(grammar, sequence, structure)
    productions = updateProbabilities(grammar)
    printProductions(productions)
        #keys = countDict.keys()
        #for key in keys

def insideOutsideLoop(grammar, sequence, structure):

    aTable = insideLoop(grammar, sequence, structure)
    #printTable(aTable)
    bTable = outsideLoop(grammar, sequence, structure, aTable)
    #return countDict
    #printTable(bTable)
    #productions = updateProbabilities(grammar, countDict)
    #printProductions(productions)

def updateProbabilities(productions):

    newProductions = defaultdict(lambda: defaultdict(list))
    
    singleDouble = productions.keys()

    for sd in singleDouble:
        production = productions[sd].keys()
        for p in production:
            if len(productions[sd][p]) == 1:
                newProductions[sd][p] += (productions[sd][p][0][0], 1.0)
            else:

                for rule, prob in productions[sd][p]:

                #count of specific rule for 'p' dividied by all 'p' rules
                    numerator = globalCountDict[p][rule]
                    if numerator == 0:
                        val = 0
                    else:
                        val = globalCountDict[p][rule]/sum(globalCountDict[p].values())
                    newProductions[sd][p] += (rule, val)
    return newProductions

def printTable(table):

    rows = table.keys()
    for row in rows:
        cols = table[row].keys()
        for col in cols:
            #print "***Position: (%d,%d)***" % (row, col)
            rules = table[row][col].keys()
            for rule in rules:
                val = table[row][col][rule]
                #print "rule: %s *** val: %s" % (rule, val)
                #print "rule", rule
                #print "val", val

def printProductions(productions):

    for singleDouble in productions.keys():
        for production in productions[singleDouble].keys():
            print singleDouble, production,
            print productions[singleDouble][production]



def CYK(productions, sequence, structure):
    
    n = len(sequence)

    #pdict[production][children productions] = list(position tuples)
    pDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))

    #initialization
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for i in range(n):
        for sp in productions['single'].keys():
            for baseStruct, prob in productions['single'][sp]:
                baseStructList = baseStruct.split()
                base = baseStructList[0]
                #print 
                #print "base:", base
                #print "struct:", struct
                #print "base (from sequence):", sequence[i]
                #print "struct (from sequence):", structure[i]
                if sequence[i] == base:
                    table[i][i][sp] = prob
                    #print table[i][i][sp]
                    #print sp
                    
                    #pDict[sp][baseStruct] += (-1, -1)
                    

    #iteration
    for i in range(1,n):
        for j in range(0,n-i):
            for k in range(0,i):
                for dp in productions['double'].keys():
                    for rule, prob in productions['double'][dp]:
                        ruleList = rule.split()
                        rule1 = ruleList[0]
                        rule2 = ruleList[1]
                        #print "rule1", rule1
                        #print "rule2", rule2
                        if rule1 in table[j][j+k].keys() and rule2 in table[j+k+1][j+i].keys():
                            val = table[j][j+k][rule1] * table[j+k+1][j+i][rule2] * prob
                            if val > table[j][j+i][dp]:
                                table[j][j+i][dp] = val
                                pDict[j][j+i][dp]["left"]["pos"] = (j,j+k)
                                pDict[j][j+i][dp]["left"]["rule"] = rule1
                                pDict[j][j+i][dp]["right"]["pos"] = (j+k+1,j+i)
                                pDict[j][j+i][dp]["right"]["rule"] = rule2



                            #print "current position: (%d, %d)" % (j, j+1)
                            #print "child1: (%d, %d)" % (j, j+k)
                            #print "child2: (%d, %d)" % (j+k+1, j+1)
                            

                            #print "HERE*********************************"
                            #if table[j][j+k][rule1] == 0:
                                #print "*************************"
                            #print "prob:", prob
                            #print "row (j):", j
                            #print "column (j+1):", j+1
                            #print "table val:", table[j][j+1][dp]

                            #pDict[dp][rule] += ((j, j+k), (j+k+1,j+1))

    #return alpha table and pointer dictionary
    #print table[0][0]
    results = traceBack(table, pDict, sequence, structure)
    structure = convertTraceToStructure(productions, results)

    return structure

def convertTraceToStructure(productions, results):

    structure = ""
    for rule in results:
        baseStruct = productions["single"][rule][0][0]
        structure += baseStruct.split()[1]
    return structure

def traceBack(CYKTable, pDict, sequence, structure):

    n = len(sequence)
    lst = []

    results = preOrder(CYKTable, pDict, (0,n-1), lst, 'F')
    return results

def preOrder(CYKTable, pDict, curPos, results, production):

    pos1 = curPos[0]
    pos2 = curPos[1]
    if (pos1 == pos2):
        results.append(production)
        return results

    leftChildPos = pDict[pos1][pos2][production]["left"]["pos"]
    leftRule = pDict[pos1][pos2][production]["left"]["rule"]
    results = preOrder(CYKTable, pDict, leftChildPos, results, leftRule)

    rightChildPos = pDict[pos1][pos2][production]["right"]["pos"]
    rightRule = pDict[pos1][pos2][production]["right"]["rule"]
    results = preOrder(CYKTable, pDict, rightChildPos, results, rightRule)

    return results


def insideLoop(productions, sequence, structure):

    n = len(sequence)

    #pdict[production][children productions] = list(position tuples)
    pDict = defaultdict(lambda: defaultdict(list))

    #initialization
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for i in range(n):
        for sp in productions['single'].keys():
            for baseStruct, prob in productions['single'][sp]:
                baseStructList = baseStruct.split()
                base = baseStructList[0]
                struct = baseStructList[1]
                #print 
                #print "base:", base
                #print "struct:", struct
                #print "base (from sequence):", sequence[i]
                #print "struct (from sequence):", structure[i]
                if sequence[i] == base and structure[i] in struct:
                    table[i][i][sp] = prob
                    #print table[i][i][sp]
                    #print sp
                    
                    #pDict[sp][baseStruct] += (-1, -1)
                    

    #iteration
    for i in range(1,n):
        for j in range(0,n-i):
            for k in range(0,i):
                for dp in productions['double'].keys():
                    for rule, prob in productions['double'][dp]:
                        ruleList = rule.split()
                        rule1 = ruleList[0]
                        rule2 = ruleList[1]
                        #print "rule1", rule1
                        #print "rule2", rule2
                        if rule1 in table[j][j+k].keys() and rule2 in table[j+k+1][j+i].keys():
                            table[j][j+i][dp] += table[j][j+k][rule1] * table[j+k+1][j+i][rule2] * prob
                            #print "current position: (%d, %d)" % (j, j+1)
                            #print "child1: (%d, %d)" % (j, j+k)
                            #print "child2: (%d, %d)" % (j+k+1, j+1)
                            

                            #print "HERE*********************************"
                            #if table[j][j+k][rule1] == 0:
                                #print "*************************"
                            #print "prob:", prob
                            #print "row (j):", j
                            #print "column (j+1):", j+1
                            #print "table val:", table[j][j+1][dp]

                            #pDict[dp][rule] += ((j, j+k), (j+k+1,j+1))

    #return alpha table and pointer dictionary
    #print table[0][0]
    return table

def outsideLoop(productions, sequence, structure, aTable):
    #loop1: for k in range(j-1, -1, -1)
        #curPos = (j,j+i)
        #parent = (k,j+i)
        #sibling = (k,j-1)
    
    #loop2: for k in range(j+i+1,n)
        #curPos = (j,j+i)
        #parent = (j,k)
        #sibling = (j+i+1,k)

    countDict = defaultdict(lambda: defaultdict(float))

    n = len(sequence)

    #initialization
    bTable = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    bTable[0][n-1]['F'] = 1
    #bTable[0][n-1]['F'] = 0.33
    #bTable[0][n-1]['S'] = 0.33
    #bTable[0][n-1]['L'] = 0.34

    #outside loop
    for i in range(n-2,-1,-1):
        for j in range(n-1-i, -1, -1):
            for k in range(j-1, -1, -1):
                #print "cur (%d,%d)" % (j,j+i),
                #print "par (%d,%d)" % (k,j+i),
                #print "sib (%d,%d)" % (k,j-1)
                for dp in aTable[k][j+i].keys():                    
                    for rule, prob in productions['double'][dp]:
                        ruleList = rule.split()
                        rule1 = ruleList[0]
                        rule2 = ruleList[1]
                           
                           #------->sibling positions         -------->current position
                        if rule1 in aTable[k][j-1].keys() and rule2 in aTable[j][j+i].keys() and bTable[k][j+i][dp] != 0:
                            #--->current position           ---->sibling position   ---->parent position
                            bTable[j][j+i][rule2] += prob * aTable[k][j-1][rule1] * bTable[k][j+i][dp]
                            #if (j==j+i):
                                #print j
                                #print rule2
                                #print bTable[j][j]
                                #print "------"
                            #--->production->rule  --->parent position  --->sibling position    --->current position
                            countDict[dp][rule] += bTable[k][j+i][dp] * aTable[k][j-1][rule1] * aTable[j][j+i][rule2]

            for k in range(j+i+1,n):
                #print "cur (%d,%d)" % (j,j+i),
                #print "par (%d,%d)" % (j,k),
                #print "sib (%d,%d)" % (j+i+1,k)

                for dp in aTable[j][k].keys(): #for each parent production

                    for rule, prob in productions['double'][dp]:
                        ruleList = rule.split()
                        rule1 = ruleList[0]
                        rule2 = ruleList[1]

                           #------->current position          -------->sibling positions
                        if rule1 in aTable[j][j+i].keys() and rule2 in aTable[j+i+1][k].keys() \
                                and bTable[j][k][dp] != 0: #current, sibling

                            #--->current position           ---->sibling position     ---->parent position
                            bTable[j][j+i][rule1] += prob * aTable[j+i+1][k][rule2] * bTable[j][k][dp]
                            #if (j == j+i):
                                #print j
                                #print bTable[j][j]
                                #print rule1
                                #print "-----"
                            #--->production->rule  --->parent position -->current position    --->sibling position
                            countDict[dp][rule] += bTable[j][k][dp] * aTable[j][j+i][rule1] * aTable[j+i+1][k][rule2]

    
    #print "*******************************************"
    #print sequence
    #print structure

    #updating countDict for terminals
    for i in range(n):
        for sp in productions['single'].keys():
            for baseStruct, prob in productions['single'][sp]:
                baseStructList = baseStruct.split()
                base = baseStructList[0]
                struct = baseStructList[1]
                if sequence[i] == base and structure[i] in struct and bTable[i][i][sp] != 0:
                    countDict[sp][baseStruct] += bTable[i][i][sp]
                    #print "countDict: %f" % (countDict[sp][baseStruct])
    
    
    #multiplying countDict by prior probability
    singleDouble = productions.keys()
    for sd in singleDouble:
        productionKeys = productions[sd].keys()
        for p in productionKeys:
            for rule, prob in productions[sd][p]:
                #countDict[p][rule] *= prob/(aTable[0][n-1]['S'] + aTable[0][n-1]['F'] + aTable[0][n-1]['L'])
                countDict[p][rule] *= prob/(aTable[0][n-1]['F'])
                globalCountDict[p][rule] += countDict[p][rule]
                #print "production %s-->%s" % (p, rule)
                #print "countDict: %f" % (countDict[p][rule])
                #print
    

    return bTable

def main():

    dataDict = parse('data.txt')
    productions = createProductions()
    #sequence = 'cgaacg'
    #structure = '((..))'
    global globalCountDict 
    globalCountDict = defaultdict(lambda: defaultdict(float))

    #insideOutsideLoop(productions, sequence, structure)
    insideOutside(productions, dataDict)

    
    ID = dataDict.keys()[1000]
    sequence = dataDict[ID]["sequence"]
    structure = dataDict[ID]["structure"]
    print "*******************************************"
    print "provided sequence: ", sequence
    print "provided structure:  ", structure

    prediction = CYK(productions, sequence, structure)
    print "predicted structure: ", prediction


main()
