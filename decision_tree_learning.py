# # overall function: I/Os are known
# # Inputs: O+, O-, table, empty DTN
# # Outputs:
import math

class DecisionTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# function 1
def candidate_predicates(T, main_attribute):
    # Initialize an empty set A to store the conditions
    A = set()

    # Assuming T is a list of dictionaries
    if not T:
        return A  # Return empty set if T is empty

    # Get the column names from the first dictionary
    columns = T[0].keys()

    for c in columns:
        # Collect unique values for the current column
        if c==main_attribute:
            continue
        unique_values = {row[c] for row in T}

        # Check the type of the column based on the first value
        if isinstance(next(iter(unique_values)), str):  # Categorical type
            for k in unique_values:
                A.add((c, '==', k))  # Add equality condition for categorical values
        elif isinstance(next(iter(unique_values)), (int, float)):  # Numerical type
            for k in unique_values:
                A.add((c, '<', k))  # Add less than condition
                A.add((c, '<=', k))  # Add less than or equal condition

    return A


# function 2 combine with max_predicate
# Calculates the information gain of a specific column of the Table
def information_gain(a, O_pos, O_neg, T):
    T_pos, T_neg = table_split(a, O_pos, O_neg, T)

    # Calculates the entropies
    s_entropy = calculate_entropy(O_pos, O_neg, T)
    l_entropy, lambda_pos = calculate_side_entropy(O_pos, O_neg, T_pos)
    r_entropy, lambda_neg = calculate_side_entropy(O_pos, O_neg, T_neg)
    
    # Calculates the information gain
    pos_coefficient = lambda_pos / (lambda_pos + lambda_neg)
    neg_coefficient = lambda_neg / (lambda_pos + lambda_neg)
    
    left_entropy = pos_coefficient * l_entropy
    right_entropy = neg_coefficient * r_entropy

    information_gain = s_entropy - (left_entropy + right_entropy)

    return information_gain


# function 3
# Divides the table into two tables based on condition a
def table_split(a, O_pos, O_neg, T):
    T_pos = []
    T_neg = []

    # Looks for the column and value of condition a
    col = a[0]
    val = a[-1]

    # If the condition is a categorical value
    if a[1] == '==':
        # Loops through all the entries of the table
        for d in range(0, len(T)):
            v = T[d][col] # Stores the value of the column of the entry being read

            # If it meets the condition append it to the positive table, if not to the negative table
            if v == val:
                T_pos.append(T[d])

            else:
                T_neg.append(T[d])

    # If the condition is a numerical value
    else:
        # For less than condition
        if len(a[1]) == 1:
            # Loops through all the entries of the table
            for d in range(0, len(T)):
                v = T[d][col] # Stores the value of the column of the entry being read

                # If it meets the condition append it to the positive table, if not to the negative table
                if v < val:
                    T_pos.append(T[d])
                else:
                    T_neg.append(T[d])

        # For less or equal than condition
        else:
            # Loops through all the entries of the table
            for d in range(0, len(T)):
                v = T[d][col] # Stores the value of the column of the entry being read

                # If it meets the condition append it to the positive table, if not to the negative table
                if v <= val:
                    T_pos.append(T[d])
                else:
                    T_neg.append(T[d])

    return T_pos, T_neg


# Calculates the total entropy
def calculate_entropy(O_pos, O_neg, T):
    O_pos_content = []
    O_neg_content = []
    O_content = []
    T_content = []

    # Loops through all the entries of the positive tuple and saves its values
    for d in range(0, len(O_pos)):
        for i in O_pos[d]:
            O_pos_content.append(O_pos[d][i])

    # Loops through all the entries of the negative tuple and saves its values
    for d in range(0, len(O_neg)):
        for i in O_neg[d]:
            O_neg_content.append(O_neg[d][i])

    # All the possible values of the column in that table
    T_content = column_values(O_pos, T)

    # Union of the output tuples
    O_content = O_pos_content + O_neg_content

    #o_len = len(O_content) # Union of output positive tuple and outpu negative tuple
    pos = 0
    neg = 0
    intersection = 0

    # Checks if the values in the postive content are in the overall content
    for x in O_pos_content:
        for o in T_content:
            if x == o:
                pos += 1

    # Checks if the values in the negative content are in the overall content
    for y in O_neg_content:
        for o in T_content:
            if y == o:
                neg += 1

    # Checks if the values in the negative content are in the overall content
    for w in O_content:
        for o in T_content:
            if w == o:
                intersection += 1

    # Calculates the total entropy of the table
    p = pos / intersection
    n = neg / intersection

    p_log = p * math.log2(p)
    n_log = n * math.log2(n)

    s_entropy = -(p_log + n_log)

    return s_entropy


# Calculates either the right or left entropy
def calculate_side_entropy(O_pos, O_neg, T):
    O_pos_content = []
    O_neg_content = []
    O_content = []
    T_content = []

    # Loops through all the entries of the positive tuple and saves its values
    for d in range(0, len(O_pos)):
        for i in O_pos[d]:
            col = i
            O_pos_content.append(O_pos[d][i])

    # Loops through all the entries of the negative tuple and saves its values
    for d in range(0, len(O_neg)):
        for i in O_neg[d]:
            O_neg_content.append(O_neg[d][i])

    # All the possible values of the column in that table
    T_content = column_values(O_pos, T)

    # Union of the output tuples
    O_content = O_pos_content + O_neg_content

    #o_len = len(O_content) # Amount of different values in O
    #if o_len == 0:  # Prevent division by zero
    #    return 0, 0
    pos = 0
    neg = 0
    intersection = 0

    # Checks if the values in the postive content are in the overall content
    for x in O_pos_content:
        for o in T_content:
            if x == o:
                pos += 1

    # Checks if the values in the negative content are in the overall content
    for y in O_neg_content:
        for o in T_content:
            if y == o:
                neg += 1

    # Checks if the values in the union are in the overall content
    for w in O_content:
        for o in T_content:
            if w == o:
                intersection += 1

    if intersection == 0:
        return 0, intersection

    else:
        # Calculates the entropy
        p = pos / intersection
        n = neg / intersection

        p_log = p * math.log2(p) if p > 0 else 0
        n_log = n * math.log2(n) if n > 0 else 0
        entropy = -(p_log + n_log)

        return entropy, intersection


# function 4, 5, 6 combined
# Calculates all the possible values for the column in the table
def column_values(O_pos, T):
    O_content = []
    # Loops through all the entries of the positive tuple and saves its values
    for d in range(0, len(O_pos)):
        for i in O_pos[d]:
            col = i

    # Loops through all the entries of the table and saves its values
    for d in range(0, len(T)):
        v = T[d][col]
        exists = False

        # Appends the value to the O content tuple if it does not exists
        if len(O_content) == 0:
            O_content.append(v)

        else:
            for i in O_content:
                if v == i:
                    exists = True

            if exists == False:
                O_content.append(v)
    return O_content


# function 2 IG function is used in here
def max_predicate(column_values, O_pos, O_neg, T):
    predicates_ig = []

    # find the information gains for all of the predicates
    for a in column_values:
        x = information_gain(a, O_pos, O_neg, T)
        predicates_ig.append((a, x))

    p = predicates_ig[0] # max predicate 
    # pos = 0
    # max_ig = p[1] max predicate information gain

    # for i in range(1, len(predicates_ig)):
    #     p = predicates_ig[i]

    #     if p[1] > max_ig:
    #         max_ig = p[1]
    #         pos = i
    # find the maximum information gain
    for i in range(1, len(predicates_ig)):
        if predicates_ig[i][1] > p[1]:
            p = predicates_ig[i]

    # p = predicates_ig[pos]
    return p
#max predicate 반환값 tuple:
# predicate[0] is the name of the predicate or what would be equivalent to a
# predicate[1] is the information gain value

def intersection(O_tuple, T_content):
    intersection_tuple = []

    # Checks for the values that are part of both the output tuple and the table
    for o in O_tuple:
        for key, value in o.items():
            if value in T_content:
                intersection_tuple.append(o)

    return intersection_tuple

def global_DTL(T, N, O_pos, O_neg):
    O_question = O_pos

    def DTL(T, N, O_pos, O_neg):
        nonlocal O_question
        #(1)
        if len(O_pos)==0:
            N.value='X'
            return N
        #(2)
        if len(O_neg)==0:
            N.value='✓' if O_pos==O_question else 'X'
            return N

        if O_pos:
            main_attribute = list(O_pos[0].keys())[0]

        # (3) (4)
        extracted_predicates = candidate_predicates(T, main_attribute)

        # (6) 안에서 # (5)도 진행
        maximum_predicate = max_predicate(extracted_predicates, O_pos, O_neg, T)
        condition, info_gain = maximum_predicate
        # print("condition, info_gain: ", condition, info_gain, "\n")
        if info_gain == 0:
            N.value='?'
            return N

        # (7) (8)

        T_pos, T_neg = table_split(condition, O_pos, O_neg, T)
        # print("T_pos: ", T_pos)
        # print("T_neg: ", T_neg)
        N.value = condition

        T_pos_content = column_values(O_pos, T_pos)
        T_neg_content = column_values(O_pos, T_neg)

        # print("\ncreating node")
        # print("creatind left node with intersection function: ", intersection(O_pos, T_pos_content), intersection(O_neg, T_pos_content))
        # print("creatind right node with intersection function: ", intersection(O_pos, T_neg_content), intersection(O_neg, T_neg_content))
        # print("N.value: ", N.value)
        N.left = DTL(T_pos, DecisionTreeNode(), intersection(O_pos, T_pos_content), intersection(O_neg, T_pos_content))
        N.right = DTL(T_neg, DecisionTreeNode(), intersection(O_pos, T_neg_content), intersection(O_neg, T_neg_content))
        return N
    return DTL(T, N, O_pos, O_neg)

def printTree(N):
    if N is None:
        return
    print(N.value)
    printTree(N.left)
    printTree(N.right)

def main():
    # the table is a list of dictionaries: [{"name": abc, "age": 45}, {"name": xyz, "age": 30}......]

    T = [
        {"studentID": "Alice", "deptCode": "Comp.", "courseID": 201, "school": "Engineering"},
        {"studentID": "Alice", "deptCode": "Chem.", "courseID": 310, "school": "Arts and Science"},
        {"studentID": "Alice", "deptCode": "Mech.", "courseID": 550, "school": "Engineering"},
        {"studentID": "Bob", "deptCode": "Mech.", "courseID": 320, "school": "Engineering"},
        {"studentID": "Bob", "deptCode": "Mech.", "courseID": 550, "school": "Engineering"},
        {"studentID": "Charlie", "deptCode": "Chem.", "courseID": 310, "school": "Arts and Science"},
        {"studentID": "David", "deptCode": "Comp.", "courseID": 500, "school": "Engineering"},
        {"studentID": "David", "deptCode": "Mech.", "courseID": 502, "school": "Engineering"},
        {"studentID": "Erin", "deptCode": "Chem.", "courseID": 310, "school": "Arts and Science"},
    ]
    T2 = [
        {"studentID": "Alice", "deptCode": "Chem."},
        {"studentID": "Bob", "deptCode": "Comp."},
        {"studentID": "Charlie", "deptCode": "Math."},
        {"studentID": "David", "deptCode": "Chem."},
        {"studentID": "Erin", "deptCode": "Mech."},
    ]
    N = DecisionTreeNode()
    N2 = DecisionTreeNode()
    """
    O_pos = [{"name": "abc"}]
    O_neg = [{"name": "xyz"}]
    """
    O_pos = [{"studentID": "Alice"}, {"studentID": "Bob"}]
    O_neg = [{"studentID": "Charlie"}, {"studentID": "David"}]

    global_DTL(T, N, O_pos, O_neg)

    # column_values = candidate_predicates(T)
    # N.value = max_predicate(column_values, O_pos, O_neg, T)
    printTree(N)
    return

main()