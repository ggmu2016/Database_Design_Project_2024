import unittest
from libra import getNextContexts, joinContexts, joinTwoTables, libra, DecisionTreeNode, treeSize, Q

class TestLibraFunctions(unittest.TestCase):

    def test_getNextContexts(self):
        context = {"studentID": "Alice", "deptCode": "Comp.", "courseID": 201, "tableName": "registration"}
        result = getNextContexts(context)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, dict) for item in result))

    def test_joinContexts(self):
        context1 = {'studentID': 'Alice', 'deptCode': 'Comp.', 'courseID': 201, 'tableName': 'registration'}
        context2 = {'deptCode': 'Comp.', 'school': 'Engineering', 'tableName': 'department'}
        joined_contexts, joined_colname = joinContexts(context1, context2)
        self.assertIsInstance(joined_contexts, dict)
        self.assertEqual(joined_colname, 'deptCode')

# TODO: this test should check if the query is correct
    # def test_joinTwoTables(self):
    #     joined_context = {'studentID': 'Alice', 'deptCode': 'Comp.', 'courseID': 201, 'tableName': 'registration&department', 'joinCol': 'deptCode'}
    #     result = joinTwoTables(joined_context)

#TODO: wait for the implementation of decision_tree_learning
    # def test_libra(self):
    #     O_pos = [{"studentID": "Alice"}, {"studentID": "Bob"}]
    #     O_neg = [{"studentID": "Charlie"}, {"studentID": "David"}]
    #     result = libra(O_pos, O_neg)

    def test_treeSize(self):
        tree = DecisionTreeNode(1, DecisionTreeNode(2), DecisionTreeNode(3))
        size = treeSize(tree)
        self.assertEqual(size, 3)

#TODO: figure out how O_pos is represented for Q. It is a dictionary or a list of dictionaries?
    # def test_Q(self):
    #     O_pos = [{"studentID": "Alice"}]
    #     context = {"studentID": "Alice", "tableName": "registration&department", "joinCol": "deptCode"}
    #     tree = DecisionTreeNode("deptCode = 'Comp.'", DecisionTreeNode("yes"), DecisionTreeNode("no"))
    #     query = Q(O_pos, context, tree)
    #     expected_query = "SELECT studentID FROM registration JOIN department ON registration.deptCode=department.deptCode WHERE deptCode = 'Comp.';"
    #     self.assertEqual(query, expected_query)

if __name__ == '__main__':
    unittest.main()