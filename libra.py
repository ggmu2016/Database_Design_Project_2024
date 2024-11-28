import heapq
from query_to_table import Query2Tuple
from decision_tree_learning import global_DTL, printTree
import collections
# using a dictionary to store overall column names to tables, i.e, {col_name:[table1,...,tableN]}
columnsInTables = {"teamID": ["teams"], "name": ["teams", "players"], "city": ["teams"], "stadium": ["teams"],
                "playerID": ["players"], "position": ["players"], "age": ["players"], "teamID": ["players"],
                "matchID": ["matches"], "homeTeamID": ["matches"], "awayTeamID": ["matches"], "matchDate": ["matches"], "homeScore": ["matches"], "awayScore": ["matches"]}


def getNextContexts(context):
    """
    Args:
        context: a python dictionary, such as: {"studentID": "Alice"}
        table_name: set of names of tables where context is from, such as ["registration"]

    Returns:
        next context: list of python dictionaries

    """
    # removing tableName and common col from context
    tables = set()
    if "tableName" in context:
        tables = set(context["tableName"].split('&'))
        del context["tableName"]
    if "joinCol" in context:
        del context["joinCol"]

    nextContexts = []
    for c in context.keys():
        for table in columnsInTables[c]:
            if table not in tables:
                query = f"select * from {table} where \"{c}\" = '{context[c]}'"
                res = Query2Tuple(query, large=True)
                if res:
                    # add table name to each dictionary
                    for i in range(len(res)):
                        # convert each sqlalchemy object within list to dict
                        res_dict = dict(res[i])
                        res_dict['tableName'] = table
                        res_dict['joinCol'] = c
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
        joinedContext["joinCol"] = commonKey


    return joinedContext, commonKey


class DecisionTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# measure a tree's cardinality by the number of nodes
def treeSize(treeNode):
    if not treeNode:
        return 0
    return 1 + treeSize(treeNode.left) + treeSize(treeNode.right)

def findEntropy(tree):
    return 0

#converts each item in the tuple to a string so that we can run .join() on the tuple
def stringifyTuple(inputTuple):
    return (str(x) for x in inputTuple)

#given O+, context information, and a tree extract a query
def Q(O_pos, context, tree):
    #use O+ to extract the name of the column actually being selected
    selectedAttributes = ", ".join(list(O_pos[0].keys()))
    #first get the join and table information
    joinTables = context["tableName"].split('&')
    joinAttribute = context["joinCol"]

    #then obtain the selection predicates from the decision tree
    selectionPredicates = []
    #traversal algorithm that returns a list of the selectionPredicates on the path from the root to a checkmark
    def obtainSelectionPredicates(node, predicates): 
        if not node:
            return
        # determines if the node is a leaf or a predicate
        if node.value != "?" and node.value != "✓" and node.value != "X":
            leftPredicates = []
            rightPredicates = []
            for predicate in predicates:
                leftPredicates.append(predicate)
                rightPredicates.append(predicate)
            leftPredicates.append(' '.join(stringifyTuple(node.value)))

            if node.value[1] == "==":
                tempNode = node
                tempNode.value = (tempNode.value[0], "!=", tempNode.value[2])
                rightPredicates.append(' '.join(stringifyTuple(tempNode.value)))
            elif node.value[1] == "<":
                tempNode = node
                tempNode.value = (tempNode.value[0], ">=", tempNode.value[2])
                rightPredicates.append(' '.join(stringifyTuple(tempNode.value)))
            elif node.value[1] == "<=":
                tempNode = node
                tempNode.value = (tempNode.value[0], ">", tempNode.value[2])
                rightPredicates.append(' '.join(stringifyTuple(tempNode.value)))
            obtainSelectionPredicates(node.left, leftPredicates)
            obtainSelectionPredicates(node.right, rightPredicates)
        elif node.value == "✓":
            selectionPredicates.append(predicates)

    obtainSelectionPredicates(tree, [])
    #form the query string using the resultant information
    tablesString = f'{joinTables[0]}'
    for table in range(1, len(joinTables)):
        # join attribute should allow multiple values but we don't have that at this moment
        tablesString += f' JOIN {joinTables[table]} ON {joinTables[table - 1]}.{joinAttribute} = {joinTables[table]}.{joinAttribute}'
    
    # pick the smallest amount of selection predicates required to reach a checkmark
    shortestPredicateLength = float("inf")
    predicateString = ""
    for i in range(len(selectionPredicates)):
        if len(selectionPredicates[i]) < shortestPredicateLength:
            shortestPredicateLength = len(selectionPredicates[i])
            predicateString = ' AND '.join(selectionPredicates[i])
    queryString = f"SELECT {selectedAttributes} FROM {tablesString} WHERE {predicateString};"
    return queryString

def joinTwoTables(joined_context):
    """

    Args:
        joined_context: list of dictionaries

    Returns:

    """
    # creates the join table from T1 and T2 and saves it in the database for easy access
    table_names = joined_context["tableName"].split('&')
    join_key = joined_context["joinCol"]
    table1 = table_names[0]
    if len(table_names)>1:
        table2 = table_names[1]
        #this query string needs to be modified to join more than 2 tables
        query = f'select * from {table1} join {table2} on {table1}."{join_key}" = {table2}."{join_key}"' #we need join_key to allow multiple values
    else:
        query = f"select * from {table1}"

    res = Query2Tuple(query, large=True)
    return res

    # maybe save this result somewhere??

def checkMarkExists(node):
    if not node:
        return False
    if node.value == "✓":
        return True
    return checkMarkExists(node.left) or checkMarkExists(node.right)

def runQ(root, N, ans):
    tree_size = treeSize(root)
    cmExists = checkMarkExists(root)
    # if we still don't have an answer then just run it regardless of size conditions
    if ans == None and cmExists:
        return True
    # if the tree doesn't have a checkmark then skip the context
    if not cmExists:
        return False
    # If there is a checkmark and we have a valid answer then check the conditions as we normally would
    return tree_size <= N and findEntropy(root) == 0

def libra(O_pos, O_neg):
    """

    Args:
        O_pos:
        O_neg:
        N:

    Returns:

    """
    N = float("inf")
    init_context = O_pos[0]
    next_contexts = getNextContexts(init_context) # list of dictionaries
    L = next_contexts.copy()
    visited_tables = set()
    ans = None
    while L:
        curr_context = L.pop()
        # get next contexts for current context
        next_contexts = getNextContexts(curr_context.copy())
        for context in next_contexts:
            (joined_context, common_column) = joinContexts(curr_context.copy(), context)
            if "tableName" in joined_context and joined_context!=curr_context and joined_context["tableName"] not in visited_tables:
                L.append(joined_context)

        if len(curr_context) > N or curr_context["tableName"] in visited_tables:
            continue
        visited_tables.add(curr_context["tableName"])
        joined_table = joinTwoTables(curr_context)
        # print("WHO MADE IT")
        # print(curr_context)
        root = DecisionTreeNode()
        global_DTL(joined_table, root, O_pos, O_neg)
        # printTree(root)
        tree_size = treeSize(root)
        if runQ(root, N, ans):#tree_size <= N and findEntropy(root) == 0:
            ans = Q(O_pos, curr_context, root)
            N = tree_size

    return ans

def main():

    # ============= testing getNextContexts ===================================================================
    context = {"studentID": "Alice", "deptCode": "Comp.", "courseID": 201, "tableName": "registration"}
    #result = getNextContexts(context)
    #print(result)      # returns list of dictionaries

    # =========================================================================================================

    # ============= testing joinContexts =====================================================================
    context1 = {'studentID': 'Alice', 'deptCode': 'Comp.', 'courseID': 201, 'tableName': 'registration'}
    context2 = {'deptCode': 'Comp.', 'school': 'Engineering', 'tableName': 'department'}
    #(joined_contexts, joined_colname) = joinContexts(context1,context2)
    #print('joined_contexts: ', joined_contexts)
    #print('joined_colname: ', joined_colname)

    # ========================================================================================================

    # # ============= testing Libra =====================================================================
    # O_pos = [{"studentID": "Alice"}, {"studentID": "Bob"}]
    # O_neg = [{"studentID": "Charlie"}, {"studentID": "David"}]
    # res = libra(O_pos,O_neg)
    # print(res)
    # ========================================================================================================





    # Hyuntae's stuff
    #O_pos = Query2Tuple('SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = \'Engineering\'')
    #print(O_pos)

    departmentTable = Query2Tuple(
        'SELECT * FROM department')  # we need to decide how to convert the resultant object into something we can work with
    majorTable = Query2Tuple('SELECT * FROM major')
    registrationTable = Query2Tuple('SELECT * FROM registration')

    #print(departmentTable)
    #print(majorTable)
    #print(registrationTable)

    # positiveQuery = Query2Tuple(
    #     'SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = \'Engineering\'')
    # O_pos = set()
    # for row in positiveQuery:
    #     O_pos.add(tuple(row))
    # O_pos = list(O_pos)
    #
    # negativeQuery = Query2Tuple(
    #     'SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" >= 500 OR department."school" != \'Engineering\'')
    # O_neg = set()
    # for row in negativeQuery:
    #     if tuple(row) not in O_pos:
    #         O_neg.add(tuple(row))
    # O_neg = list(O_neg)
    #
    # print(O_pos)
    # print(O_neg)

    #libra(O_pos, O_neg)



main()