# ORC Decode program Catalina Rotaru & Freddie Starkey
import numpy
import superFixer

def orcCorrect(sequence, lexicon):
    extracted = extractORC(sequence)
    print extracted
    orcCodes = removeGaps(extracted)
    print orcCodes
    base4Orcs = convertBase4(orcCodes)
    print base4Orcs
    base10Orcs = map(base4tobase10, base4Orcs)
    print base10Orcs
    wordCode = extractword(sequence)
    print wordCode
    orcFormatWord = addA(wordCode)
    print orcFormatWord
    wordOrcCodes = getWordOrcs(orcFormatWord)
    print "wordOrcCodes" + str(wordOrcCodes)
    if check(base10Orcs, wordOrcCodes):
        return sequence
    elif correctword(orcFormatWord, base10Orcs, wordOrcCodes) == False:
        #return sequence
        return superFixer.findByORC(sequence, lexicon)
    else:
        correction = correctword(orcFormatWord, base10Orcs, wordOrcCodes)
        return sequence[:4] + correction[0] + 'CC' + correction[1:len(correction)-1] + sequence[11:]

# Extract the ORC sequence
def extractORC(sequence):
    return sequence[28:46]

#Remove the gaps and get the code from the ORC sequence
def removeGaps(orc):
    L = [1,2,3,4,5]
    code = []
    count = 0
    for i in L:
        if count % 2 == 0:
            code.append(orc[count:count+2])
        count += 4
    return code

#Convert the ORC code from DNA format into base 4
def convertBase4 (tab):
    convert4 = []
    for elem in tab:
        convert4.append(change(elem))
    return convert4

def change(elem):
    itemElem =""
    for item in elem:
        if item == 'A':
            itemElem = itemElem + '0'
        if item == 'T':
            itemElem = itemElem + '1'
        if item == 'G':
            itemElem = itemElem + '2'
        if item == 'C':
            itemElem = itemElem + '3'
    return itemElem

#Convert base 4 sequence into base 10
def base4tobase10 (tabItem):
    return int(numpy.base_repr(int(tabItem, base=4), 10))

#Extract the word from the sequence
def extractword(sequence):
    return sequence[4] + sequence[7:11]

#Add an A at the end of the word
def addA(word):
    return word + 'A'

#Do the sum of the rows from the word
def convertRows(addAword):
    row_result = []
    half1 = addAword[0:3]
    half2 = addAword[3:6]
    half1_base4 = change(half1)
    half2_base4 = change(half2)
    sum = 0
    for i in half1_base4:
        dec = int(i)
        sum += dec
    row_result.append(sum)
    sum2 = 0
    for j in half2_base4:
        dec2 = int(j)
        sum2 += dec2
    row_result.append(sum2)
    return row_result

#Do the sum of the columns from the word
def convertColumns(addAword):
    column_result = []
    first = addAword[0] + addAword[3]
    second = addAword[1] + addAword[4]
    third = addAword[2] + addAword[5]
    first_base4 = change(first)
    second_base4 = change(second)
    third_base4 = change(third)
    sum = 0
    for i in first_base4:
        dec = int(i)
        sum += dec
    column_result.append(sum)
    sum2 = 0
    for j in second_base4:
        dec2 = int(j)
        sum2 += dec2
    column_result.append(sum2)
    sum3 = 0
    for t in third_base4:
        dec3 = int(t)
        sum3 += dec3
    column_result.append(sum3)
    return column_result

#Append the rows and columns results into one array
def getWordOrcs(addAword):
    columns = convertColumns(addAword)
    rows = convertRows(addAword)
    return rows + columns

#Check if the ORC code is the same with the array made from the word
def check(orc_extracted, word_array):
    if orc_extracted == word_array:
        return True
    elif orc_extracted != word_array:
        return False

#Function for correcting the word
def correctword(word, orc_extracted, word_array):
    print "word " + str(word)
    print "orc extracted " + str(orc_extracted)
    print "word array " + str(word_array)
    orcCompare = list(enumerate(zip(orc_extracted, word_array)))
    print orcCompare
    errorLoc = [orcDigit[0] for orcDigit in orcCompare if orcDigit[1][0] != orcDigit[1][1]]
    print errorLoc
    if len(errorLoc) != 2 or (1 not in errorLoc and 0 not in errorLoc): # the strand is damaged too much for the orc to fix it
        print "too many errors for ORC"
        return False
    elif errorLoc[0] == 0:
        print 'row 1'
        fix = toDNA(abs(orc_extracted[errorLoc[1]] - wordVal(word[sum(errorLoc) + 1])))
        if fix == None:
            return False
        print fix
        wordAsList = list(word)
        wordAsList[errorLoc[1] - 2] = fix
        print wordAsList
        return ''.join(wordAsList)
    elif errorLoc[0] == 1:
        print "row 2"
        fix = toDNA(abs(orc_extracted[errorLoc[1]] - wordVal(word[errorLoc[0] + errorLoc[1] - 3])))
        if fix == None:
            return False
        print fix
        wordAsList = list(word)
        wordAsList[errorLoc[0] + errorLoc[1]] = fix
        print wordAsList
        return ''.join(wordAsList)

def wordVal(base):
    if base == 'A':
        return 0
    elif base == 'T':
        return 1
    elif base == 'G':
        return 2
    elif base == 'C':
        return 3

def toDNA(number):
    if number == 0:
        return 'A'
    elif number == 1:
        return 'T'
    elif number == 2:
        return 'G'
    elif number == 3:
        return 'C'


