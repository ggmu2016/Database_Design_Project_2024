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


def getContext(x):
    pass


N = float("inf")


def joinContexts(c1, c2, attribute):
    pass


class DecisionTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def decision_tree_learning():
    pass


def treeSize(tree):
    pass


def findEntropy(tree):
    pass


def Q():
    pass


def joinTwoTables():
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
