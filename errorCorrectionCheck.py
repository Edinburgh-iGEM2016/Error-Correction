import lexEncode
import levenshtein
import orcDecode

lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/ogdan",
                           "/home/freddie/PycharmProjects/iGEM/codeRecord",
                           "/home/freddie/PycharmProjects/iGEM/gBlocks")

def giveORC(donor, wordRegion):
    return "GGAG" + wordRegion[0] + "CC" + wordRegion[1:] + "TAGCTAATCACTTATGA" + orcDecode.extractORC(donor) + "CGCT"

lev = [[], [], [], [], []]
errors = [[], [], [], [], []]
for eachWord in lexicon:
    for eachOtherWord in lexicon:
        dist = levenshtein.levenshtein(orcDecode.extractword(eachWord[1]), orcDecode.extractword(eachOtherWord[1]))
        lev[dist - 1].append(giveORC(eachWord[1], orcDecode.extractword(eachOtherWord[1])))
    for i in xrange(5):
        errors[i].append([(eachWord[1], orcDecode.orcCorrect(sequence), sequence) for sequence in lev[i] if orcDecode.orcCorrect(sequence) != eachWord[1]])
    lev = [[], [], [], [], []]

for j in xrange(5):
    print str(len([err for err in errors[j] if err != []])) +  " " + str(len(errors[j]))













