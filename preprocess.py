with open("inputs/corpusirc.txt", "r", errors="ignore") as corpus:
    linhas = corpus.readlines()

with open("inputs/corpusircfiltered.txt", "a", errors="ignore") as corpus:
    for l in linhas:
        if l.count(">") > 0:
            l_split = l.split(">")
        corpus.write(l_split[1])




