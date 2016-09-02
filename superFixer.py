#import lexEncode
import levenshtein
import orcDecode

#lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/ogdan",
                           #"/home/freddie/PycharmProjects/iGEM/codeRecord",
                           #"/home/freddie/PycharmProjects/iGEM/gBlocks")

def findByORC(wordToFix, lexicon):
    sameORC = [seq[1][4] + seq[1][7:11] for seq in lexicon if orcDecode.extractORC(seq[1]) == orcDecode.extractORC(wordToFix)]
    print sameORC
    word = orcDecode.extractword(wordToFix)
    levDist = [levenshtein.levenshtein(word, possible) for possible in sameORC]
    print levDist
    levPerPossible = min(zip(sameORC, levDist), key=lambda x: x[1])
    print levPerPossible
    return wordToFix[:4] + levPerPossible[0][0] + 'TT' + levPerPossible[0][1:] + wordToFix[11:]
