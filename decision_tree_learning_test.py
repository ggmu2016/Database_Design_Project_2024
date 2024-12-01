import unittest
from decision_tree_learning import DecisionTreeNode, DTL, candidate_predicates, information_gain, table_split, calculate_entropy, calculate_side_entropy, column_values, max_predicate, intersection

class TestDecisionTreeLearning(unittest.TestCase):

    def setUp(self):
        self.T = [
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
        self.O_pos = [{"studentID": "Alice"}, {"studentID": "Bob"}]
        self.O_neg = [{"studentID": "Charlie"}, {"studentID": "David"}]

    def test_candidate_predicates(self):
        predicates = candidate_predicates(self.T)
        self.assertTrue(('deptCode', '==', 'Comp.') in predicates)
        self.assertTrue(('courseID', '<', 310) in predicates)
        self.assertTrue(('courseID', '<=', 310) in predicates)

# TODO: check one information gain calculation
    def test_information_gain(self):
        a = ('courseID', '<', 500)
        ig = information_gain(a, self.O_pos, self.O_neg, self.T)
        self.assertIsInstance(ig, float)
        self.assertEqual(ig, 0.09436)

    def test_table_split(self):
        a = ('deptCode', '==', 'Comp.')
        T_pos, T_neg = table_split(a, self.O_pos, self.O_neg, self.T)
        self.assertEqual(len(T_pos), 2)
        self.assertEqual(len(T_neg), 7)

# TODO: check one entropy calculation
    def test_calculate_entropy(self):
        entropy = calculate_entropy(self.O_pos, self.O_neg, self.T)
        self.assertIsInstance(entropy, float)

# TODO: check one entropy calculation
    def test_calculate_side_entropy(self):
        entropy, intersection = calculate_side_entropy(self.O_pos, self.O_neg, self.T)
        self.assertIsInstance(entropy, float)
        self.assertIsInstance(intersection, int)

    def test_column_values(self):
        values = column_values(self.O_pos, self.T)
        self.assertIn("Alice", values)
        self.assertIn("Bob", values)

# TODO: check one max predicate calculation
    def test_max_predicate(self):
        predicates = candidate_predicates(self.T)
        max_pred = max_predicate(predicates, self.O_pos, self.O_neg, self.T)
        self.assertIsInstance(max_pred, tuple)
        self.assertEqual(len(max_pred), 2)

    def test_intersection(self):
        T_content = column_values(self.O_pos, self.T)
        intersect = intersection(self.O_pos, T_content)
        self.assertEqual(len(intersect), 2)
        self.assertEqual([{"studentID": "Alice"}, {'studentID': 'Bob'}], intersect)

# TODO: add output check
    def test_DTL(self):
        N = DecisionTreeNode()
        tree = DTL(self.T, N, self.O_pos, self.O_neg)
        self.assertIsInstance(tree, DecisionTreeNode)
        self.assertIsNotNone(tree.value)

if __name__ == '__main__':
    unittest.main()