import heapq
from query_to_table import Query2Tuple

# using a dictionary to store overall column names to tables, i.e, {col_name:[table1,...,tableN]}
columnsInTables = {"studentID": ["registration", "major"], "deptCode": ["registration", "major"],
                   "courseID": ["registration"],
                   "school": ["department"]}


def getNextContexts(context, table_name):
    """
    Args:
        context: a python dictionary, such as: {"studentID": "Alice"}
        table_name: set of names of tables where context is from, such as ["registration"]

    Returns:
        next context: list of python dictionaries
    """
    nextContexts = []
    for c in context.keys():
        for table in columnsInTables[c]:
            if table not in table_name:
                query = f"select * from {table} where \"{c}\" = '{context[c]}'"
                res = Query2Tuple(query)
                if res:
                    # add table name to each dictionary
                    for i in range(len(res)):
                        # convert each sqlalchemy object within list to dict
                        res_dict = dict(res[i])
                        res_dict['tableName'] = table
                        nextContexts.append(res_dict)
    return nextContexts



def joinContexts(context1, context2):
    """

    Args:
        context1: python dictionary  {col_name: value}
        context2: python dictionary  {col_name: value}

    Returns: joined contexts and the column name that joins them together

    """
    joinedContext = context1   # dictionary
    commonKey = None
    for key in context1.keys():
        if key in context2 and context1[key]==context2[key] and context1['tableName']!=context2['tableName']:
            commonKey = key
            break

    # join the dicts together
    for key, val in context2.items():
        if commonKey and key!=commonKey and key not in context1 and key!="tableName":
            joinedContext[key] = val

    # rename tableName to joint table name
    if commonKey:
        joinedContext["tableName"]= context1["tableName"] + "&" + context2["tableName"]


    return joinedContext, commonKey


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


def joinTwoTables(joined_context, common_column):
    """

    Args:
        joined_context: list of dictionaries

    Returns:

    """
    # creates the join table from T1 and T2 and saves it in the database for easy access
    table_names = joined_context["tableName"].split('&')
    table1 = table_names[0]
    if len(table_names)>1:
        table2 = table_names[1]

    query = f"select * from {table1} join {table2} on {common_column}"
    res = Query2Tuple(query)

    # maybe save this result somewhere??


def libra(O_pos, O_neg, N):
    """

    Args:
        O_pos:
        O_neg:
        N:

    Returns:

    """
    init_context = O_pos[0]
    table_name = set()
    contexts = getNextContexts(init_context, table_name) # list of dictionaries
    L = contexts.copy()
    #heapq.heapify(L)
    while L:
        curr_context = L.pop()
        if len(curr_context) > N:
            continue
        (joined_contexts, common_column) = joinContexts(init_context, curr_context)
        joined_table = joinTwoTables(joined_contexts,common_column)
        T = DecisionTreeNode()
        tree = decision_tree_learning(T_c, T, O_pos, O_neg)
        if treeSize(tree) <= N and findEntropy(tree) == 0:
            ans = Q(T_c, tree)
            N = treeSize(tree)
        for context in c:
            L = joinTwoTables()
    return ans

def main():
    #O_pos = Query2Tuple('SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = \'Engineering\'')
    #print(O_pos)

    # testing getNextContexts
    context = {"studentID": "Alice"}
    table_name = set()
    result = getNextContexts(context, table_name)
    #print(result)      # returns list of dictionaries


    # testing joinContexts
    context1 = {'studentID': 'Alice', 'deptCode': 'Comp.', 'courseID': 201, 'tableName': 'registration'}
    context2 = {'deptCode': 'Comp.', 'school': 'Engineering', 'tableName': 'department'}
    (joined_contexts, joined_colname) = joinContexts(context1,context2)
    #print('joined_contexts: ', joined_contexts)
    #print('joined_colname: ', joined_colname)

    # Hyuntae's stuff
    departmentTable = Query2Tuple(
        'SELECT * FROM department')  # we need to decide how to convert the resultant object into something we can work with
    majorTable = Query2Tuple('SELECT * FROM major')
    registrationTable = Query2Tuple('SELECT * FROM registration')

    #print(departmentTable)
    #print(majorTable)
    #print(registrationTable)

    positiveQuery = Query2Tuple(
        'SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = \'Engineering\'')
    O_pos = set()
    for row in positiveQuery:
        O_pos.add(tuple(row))
    O_pos = list(O_pos)

    negativeQuery = Query2Tuple(
        'SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" >= 500 OR department."school" != \'Engineering\'')
    O_neg = set()
    for row in negativeQuery:
        if tuple(row) not in O_pos:
            O_neg.add(tuple(row))
    O_neg = list(O_neg)

    print(O_pos)
    print(O_neg)

    #libra(O_pos, O_neg)



main()