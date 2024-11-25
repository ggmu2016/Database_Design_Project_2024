from query_to_table import Query2TupleLarge
from libra import libra
import unittest

class TestQueryToTable(unittest.TestCase):
    def setUp(self):
        self.queries = [
            "SELECT * FROM team;",
            "SELECT name FROM team;",
            "SELECT team.name, player.name FROM team JOIN player on team.teamID=player.teamID;",
            "SELECT name FROM team WHERE city='Dylanside';",
            "SELECT players.name FROM players JOIN teams ON players.teamID = teams.teamID WHERE teams.city = 'Dylanside';",
            "SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore > 3;",
            "SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore > 3 and awayScore < 2;",
            "SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore > awayScore;",
            "SELECT player.name FROM team JOIN  players JOIN matches on teamID=homeTeamID WHERE homeScore > awayScore and position='Forward';",
            "SELECT home_team.name, away_team.name, matches.homeScore, matches.awayScore FROM matches JOIN teams AS home_team ON matches.homeTeamID = home_team.teamID JOIN teams AS away_team ON matches.awayTeamID = away_team.teamID WHERE matches.homeScore > matches.awayScore;"
        ]
    # TODO: figure out O_neg

    def test_query0(self):
        O_pos = Query2TupleLarge(self.queries[0])
        O_neg = []
        self.assertEqual(self.queries[0], libra(O_pos, O_neg))

    def test_query1(self):
        O_pos = Query2TupleLarge(self.queries[1])
        O_neg = []
        self.assertEqual(self.queries[1], libra(O_pos, O_neg))

    def test_query2(self):
        O_pos = Query2TupleLarge(self.queries[2])
        O_neg = []
        self.assertEqual(self.queries[2], libra(O_pos, O_neg))
    
    def test_query3(self):
        O_pos = Query2TupleLarge(self.queries[3])
        O_neg = Query2TupleLarge("SELECT * FROM team WHERE city!='Dylanside")
        self.assertEqual(self.queries[3], libra(O_pos, O_neg))
    
    def test_query4(self):
        O_pos = Query2TupleLarge(self.queries[4])
        O_neg = Query2TupleLarge("SELECT players.name FROM players JOIN teams ON players.teamID = teams.teamID WHERE teams.city != 'Dylanside';")
        self.assertEqual(self.queries[4], libra(O_pos, O_neg))
    
    def test_query5(self):
        O_pos = Query2TupleLarge(self.queries[5])
        O_neg = Query2TupleLarge("SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore <= 3;")
        self.assertEqual(self.queries[5], libra(O_pos, O_neg))
    
    def test_query6(self):
        O_pos = Query2TupleLarge(self.queries[6])
        O_neg = Query2TupleLarge("SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore <= 3 or awayScore >= 2;")
        self.assertEqual(self.queries[6], libra(O_pos, O_neg))
    
    def test_query7(self):
        O_pos = Query2TupleLarge(self.queries[7])
        O_neg = Query2TupleLarge("SELECT teamName FROM team JOIN  matches on teamID=homeTeamID WHERE homeScore <= awayScore;")
        self.assertEqual(self.queries[7], libra(O_pos, O_neg))
    
    def test_query8(self):
        O_pos = Query2TupleLarge(self.queries[8])
        O_neg = Query2TupleLarge("SELECT player.name FROM team JOIN  players JOIN matches on teamID=homeTeamID WHERE homeScore <= awayScore and position!='Forward';")
        self.assertEqual(self.queries[8], libra(O_pos, O_neg))
    
    def test_query9(self):
        O_pos = Query2TupleLarge(self.queries[9])
        O_neg = Query2TupleLarge("SELECT home_team.name, away_team.name, matches.homeScore, matches.awayScore FROM matches JOIN teams AS home_team ON matches.homeTeamID = home_team.teamID JOIN teams AS away_team ON matches.awayTeamID = away_team.teamID WHERE matches.homeScore <= matches.awayScore;")
        self.assertEqual(self.queries[9], libra(O_pos, O_neg))

