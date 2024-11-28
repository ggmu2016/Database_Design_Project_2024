from query_to_table import Query2TupleLarge
from libra import libra
import unittest

class TestQueryToTable(unittest.TestCase):
    def setUp(self):
        self.queries = [
            "SELECT * FROM teams;",
            "SELECT name FROM teams;",
            "SELECT teams.name, players.name FROM teams JOIN players on teams.\"teamID\"=players.\"teamID\";",
            "SELECT name FROM teams WHERE city='Dylanside';",
            "SELECT players.name FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE teams.city = 'Dylanside';",
            "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > 3;",
            "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > 3 and \"awayScore\" < 2;",
            "SELECT name FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > \"awayScore\";",
            "SELECT player.name FROM teams JOIN  players JOIN matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" > \"awayScore\" and position='Forward';",
            "SELECT home_team.name, away_team.name, matches.\"homeScore\", matches.\"awayScore\" FROM matches JOIN teams AS home_team ON matches.\"homeTeamID\" = home_team.\"teamID\" JOIN teams AS away_team ON matches.\"awayTeamID\" = away_team.\"teamID\" WHERE matches.\"homeScore\" > matches.\"awayScore\";"
        ]
    # TODO: figure out O_neg

    # def test_query0(self):
    #     O_pos = Query2TupleLarge(self.queries[0])
    #     O_neg = []
    #     self.assertEqual(self.queries[0], libra(O_pos, O_neg))

    # def test_query1(self):
    #     O_pos = Query2TupleLarge(self.queries[1])
    #     O_neg = []
    #     self.assertEqual(self.queries[1], libra(O_pos, O_neg))

    # def test_query2(self):
    #     O_pos = Query2TupleLarge(self.queries[2])
    #     O_neg = []
    #     self.assertEqual(self.queries[2], libra(O_pos, O_neg))
    
    # def test_query3(self): 
    #     O_pos = Query2TupleLarge(self.queries[3])
    #     O_neg = Query2TupleLarge("SELECT name FROM teams WHERE city!='Dylanside'")
    #     self.assertEqual(self.queries[3], libra(O_pos, O_neg))
    
    # def test_query4(self): # returns None
    #     O_pos = Query2TupleLarge(self.queries[4])
    #     O_neg = Query2TupleLarge("SELECT players.name FROM players JOIN teams ON players.\"teamID\" = teams.\"teamID\" WHERE teams.city != 'Dylanside';")
    #     self.assertEqual(self.queries[4], libra(O_pos, O_neg))
    
    # def test_query5(self): # division by 0 error
    #     O_pos = Query2TupleLarge(self.queries[5])
    #     O_neg = Query2TupleLarge("SELECT \"name\" FROM teams JOIN  matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" <= 3;")
    #     self.assertEqual(self.queries[5], libra(O_pos, O_neg))
    
    # def test_query6(self): # division by 0 error
    #     O_pos = Query2TupleLarge(self.queries[6])
    #     O_neg = Query2TupleLarge("SELECT name FROM teams JOIN matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" <= 3 or \"awayScore\" >= 2;")
    #     self.assertEqual(self.queries[6], libra(O_pos, O_neg))
    
    # def test_query7(self): # division by 0 error
    #     O_pos = Query2TupleLarge(self.queries[7])
    #     O_neg = Query2TupleLarge("SELECT name FROM teams JOIN matches on \"teamID\"=\"homeTeamID\" WHERE \"homeScore\" <= \"awayScore\";")
    #     self.assertEqual(self.queries[7], libra(O_pos, O_neg))
    
    # def test_query8(self):
    #     O_pos = Query2TupleLarge(self.queries[8])
    #     O_neg = Query2TupleLarge("SELECT player.name FROM team JOIN  players JOIN matches on teamID=homeTeamID WHERE homeScore <= awayScore and position!='Forward';")
    #     self.assertEqual(self.queries[8], libra(O_pos, O_neg))
    
    # def test_query9(self):
    #     O_pos = Query2TupleLarge(self.queries[9])
    #     O_neg = Query2TupleLarge("SELECT home_team.name, away_team.name, matches.homeScore, matches.awayScore FROM matches JOIN teams AS home_team ON matches.homeTeamID = home_team.teamID JOIN teams AS away_team ON matches.awayTeamID = away_team.teamID WHERE matches.homeScore <= matches.awayScore;")
    #     self.assertEqual(self.queries[9], libra(O_pos, O_neg))

if __name__ == '__main__':
    unittest.main()
