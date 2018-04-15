import sqlite3

dbconnection = None
dbcursor = None
dirtymoves = 0
database = {}
movedbfile = 'data/move-database.db'


def hashNodes(node):
    """
    Compute a hash of node to store in our move database.
    >>> hashNodes([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
    '1,2,4,4,5,6,0,12,11,10,9,8,7,0,0'
    """
    return ",".join([str(n) for n in node])


def saveMoveDB():
    dbconnection.commit()


def loadMoveDB():
    global dbconnection
    global dbcursor
    dbconnection = sqlite3.connect(movedbfile)
    dbcursor = dbconnection.cursor()
    dbcursor.executescript('''CREATE TABLE IF NOT EXISTS Nodes
                        (nodehash text PRIMARY KEY, depth int,
                         score int, bestmove text)
                     ''')


def memorizeState(node, depth, score, bestMove):
    global dbcursor
    if dbcursor is None:
        return
    nodehash = hashNodes(node)
    best = ','.join([str(x) for x in bestMove])
    dbcursor.execute('''DELETE FROM Nodes WHERE nodehash=:nodehash;''',
                     {"nodehash": nodehash})
    dbcursor.execute('''INSERT INTO Nodes (nodehash, depth, score, bestmove)
                     VALUES (:nodehash, :depth, :score, :bestmove); ''',
                     {"nodehash": nodehash, "depth": depth, "score": score,
                      "bestmove": best})
    dbconnection.commit()


def recallState(node):
    global dbcursor
    if dbcursor is None:
        return None
    nodehash = hashNodes(node)
    dbcursor.execute('''SELECT depth, score, bestmove from Nodes WHERE
            nodehash=?''', (nodehash,))
    row = dbcursor.fetchone()
    parsed = None
    best = None
    if row:
        if row[2]:
            best = [int(x) for x in row[2].split(',')]
        parsed = (int(row[0]), int(row[1]), best)
    return parsed
