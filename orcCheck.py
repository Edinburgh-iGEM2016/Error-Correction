import lexEncode
import levenshtein
import orcDecode

lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/ogdan",
                           "/home/freddie/PycharmProjects/iGEM/codeRecord",
                           "/home/freddie/PycharmProjects/iGEM/gBlocks")

def giveORC(donor, wordRegion):
    return "GGAG" + wordRegion[0] + "CC" + wordRegion[1:] + "TAGCTAATCACTTATGA" + orcDecode.extractORC(donor) + "CGCT"

lev1 = []
errors = []
for eachWord in lexicon:
    for eachOtherWord in lexicon:
        if levenshtein.levenshtein(orcDecode.extractword(eachWord[1]), orcDecode.extractword(eachOtherWord[1])) == 2:
            lev1.append(giveORC(eachWord[1], orcDecode.extractword(eachOtherWord[1])))
    errors.append([(eachWord[1], orcDecode.orcCorrect(sequence), sequence) for sequence in lev1 if orcDecode.orcCorrect(sequence) != eachWord[1]])
    lev1 = []

errRecord = open("/home/freddie/PycharmProjects/iGEM/errRecord.txt", "rw+")
errRecord.truncate()
for eachErr in [err for err in errors if err != []]:
    errRecord.write("%s\n" % str(eachErr))
errRecord.close()






