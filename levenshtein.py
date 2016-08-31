# from Rosetta Code, some small editing by Freddie Starkey

def levenshtein(compare1, compare2):
    if len(compare1) > len(compare2):
        compare1 = compare2
        compare2 = compare1
    dist = xrange(len(compare1) + 1)
    for index2, char2 in enumerate(compare2):
        newDist = [index2 + 1]
        for index1, char1 in enumerate(compare1):
            if char1 == char2:
                newDist.append(dist[index1])
            else:
                newDist.append(1 + min((dist[index1],
                                        dist[index1 + 1],
                                        newDist[-1])))
        dist = newDist
    return dist[-1]
