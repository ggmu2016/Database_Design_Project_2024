import heapq
from query_to_table import Query2Tuple

# using a dictionary to store overall column names to tables, i.e, {col_name:[table1,...,tableN]}
columnsInTables = {"studentID": ["registration", "major"], "deptCode": ["registration", "major"],
                   "courseID": ["registration"],
                   "school": ["department"]}


def getNextContexts(context: tuple[str or int], cols: tuple[str], table_name: set[str]):
    """
    Args:
        context: a single tuple of string or int values, such as: (Alice,Comp.,201)
        cols: tuple of names of columns (strings), such as ("studentID","deptCode", "courseID")
        table_name: set of names of tables where context is from, such as ["registration"]

    Returns:
        next context: list of tuples
    """
    nextContexts = []
    for index, c in enumerate(cols):
        for table in columnsInTables[c]:
            if table not in table_name:
                query = f"select * from {table} where {c == context[index]}"
                res = Query2Tuple(query)
                if res:
                    nextContexts.append(res)
    return nextContexts

N = float("inf")


def joinContexts(context1, context2, cols1, cols2):
    """

    Args:
        context1: tuple
        context2: tuple
        cols1: names of the columns of context 1 (list of strings)
        cols2: names of the columns of context 2 (list of strings)

    Returns: joined context (tuple?) and the column name that joins them together

    """
    context1, context2 = list(context1), list(context2)
    joinedContext = context1
    for i, c1 in enumerate(context1):
        for j, c2 in enumerate(context2):
            if cols1[i] == cols2[j] and c1 == c2:
                j_stop = j
                break
    joinedContext.extend(context2[0:j_stop])
    if j_stop != (len(context2) - 1):
        joinedContext.extend(context2[j_stop + 1:len(context2)])

    return tuple(joinedContext), cols2[j_stop]


class DecisionTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right



def treeSize(tree):
    pass


def findEntropy(tree):
    pass


def Q():
    pass


def joinTwoTables(T1, T2, colName):
    # creates the join table from T1 and T2 and saves it in the database for easy access
    query = f"select * from {T1} join {T2} on {colName}"
    pass


def libra(O_pos: tuple[str or int], O_neg: tuple[str or int]):
    x = O_pos[1]
    context = getContext(x)
    L = context.copy()
    heapq.heapify(L)
    while L:
        c = heapq.heappop(L)
        if len(c) > N:
            break
        T_c = joinContexts(c1, c2, attribute)
        T = DecisionTreeNode()
        tree = decision_tree_learning(T_c, T, O_pos, O_neg)
        if treeSize(tree) <= N and findEntropy(tree) == 0:
            ans = Q(T_c, tree)
            N = treeSize(tree)
        for context in c:
            L = joinTwoTables()
    return ans
