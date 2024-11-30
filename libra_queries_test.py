from query_to_table import Query2TupleLarge
from libra import libra
import unittest

class TestQueryToTable(unittest.TestCase):
    def setUp(self):
        self.queries = [
            "SELECT * FROM teams;",
            "SELECT \"teamName\" FROM teams;",
            "SELECT teams.\"teamName\", players.\"playerName\" FROM teams JOIN players on teams.\"teamID\"=players.\"teamID\";",
            "SELECT \"teamName\" FROM teams WHERE city='Brandonport';",
            "SELECT players.\"playerName\", teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE teams.city = 'Brandonport';",
            "SELECT players.\"playerName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE age<26 and \"teamName\"='Prince Group';",
            "SELECT DISTINCT teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE age>33;",
            "SELECT DISTINCT \"teamName\" FROM teams JOIN merchandise ON teams.\"teamID\" = merchandise.\"teamID\" WHERE price>70;",
            # "SELECT DISTINCT players.\"playerName\", teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE position='Defender';",
            "SELECT DISTINCT players.\"playerName\" FROM players WHERE position='Goalkeeper';",
            "SELECT DISTINCT teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" JOIN merchandise ON teams.\"teamID\"=merchandise.\"teamID\" WHERE age>33 and price>70;"
            ]
    
    def get_O_neg_query(self, query):
        selection_str = query.split("WHERE")[0]
        selected_cols = selection_str.split("SELECT")[1].split("FROM")[0].replace(" DISTINCT", "")
        if len(selected_cols.split(",")):
            selected_cols = f' ({selected_cols.strip()}) '
        query = query.replace(";","")
        return f'{selection_str}WHERE{selected_cols}NOT IN ({query});' 
    
    def check_query(self, O_pos, O_neg, query):
        res = Query2TupleLarge(query)
        pos = set(res).issubset(set(O_pos))
        neg = not bool(set(res) & set(O_neg))
        return pos and neg if len(O_neg) > 0 else pos

    def test_query0(self): # works
        O_pos = Query2TupleLarge(self.queries[0])
        O_neg = []
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))

    def test_query1(self): 
        O_pos = Query2TupleLarge(self.queries[1])
        O_neg = []
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))

    def test_query2(self): 
        O_pos = Query2TupleLarge(self.queries[2])
        O_neg = []
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))

    def test_query3(self): 
        O_pos = Query2TupleLarge(self.queries[3])
        O_neg = Query2TupleLarge("SELECT \"teamName\" FROM teams WHERE city!='Brandonport'")
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
    
    def test_query4(self): 
        O_pos = Query2TupleLarge(self.queries[4])
        O_neg = Query2TupleLarge("SELECT players.\"playerName\", teams.\"teamName\" FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE teams.city != 'Brandonport';")
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
    
    def test_query5(self): 
        O_pos = Query2TupleLarge(self.queries[5])
        O_neg = Query2TupleLarge(self.get_O_neg_query(self.queries[5]))
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
    
    def test_query6(self): 
        O_pos = Query2TupleLarge(self.queries[6])
        O_neg = Query2TupleLarge(self.get_O_neg_query(self.queries[6]))
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
   
    def test_query7(self): 
        O_pos = Query2TupleLarge(self.queries[7])
        O_neg = Query2TupleLarge(self.get_O_neg_query(self.queries[7]))
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
    
    def test_query8(self): 
        O_pos = Query2TupleLarge(self.queries[8])
        O_neg = Query2TupleLarge(self.get_O_neg_query(self.queries[8]))
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))
    
    def test_query9(self): 
        O_pos = Query2TupleLarge(self.queries[9])
        O_neg = Query2TupleLarge(self.get_O_neg_query(self.queries[9]))
        self.assertTrue(self.check_query(O_pos, O_neg, libra(O_pos, O_neg)))

if __name__ == '__main__':
    unittest.main()
