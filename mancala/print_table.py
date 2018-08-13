CELL_WIDTH = 10


def makeHeader(names):
    headers = []
    header = [formatCell(n, '>') for n in [''] + names]
    headers.append('|'.join([''] + header + ['']))
    headers.append(
        '|'.join(
            [''] +
            [':' + '-' * (CELL_WIDTH - 1)] +
            (['-' * (CELL_WIDTH - 1) + ':'] * len(names)) +
            ['']))
    return headers


def formatCell(x, align='>'):
    fmt = '{0: ' + str(align) + str(CELL_WIDTH) + '}'
    return fmt.format(x)


def formatStats(t, w, l, i, j):
    s = t + w + l
    pct = int(w / max(1, s) * 100)
    return '' if i == j else formatCell(pct, '>')


def printTable(results, names):
    numPlayers = len(names)
    for h in makeHeader(names):
        print(h)
    for i in range(numPlayers):
        res = [formatStats(*c, i, j) for j, c in enumerate(results[i])]
        row = [formatCell(n, '>') for n in [names[i]] + res]
        print('|'.join([''] + row + ['']))
