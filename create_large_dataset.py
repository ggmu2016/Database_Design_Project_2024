from sqlalchemy import create_engine, Column, String, Integer, CHAR, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Engine for our own large dataset, randomly generated using python Faker library
largeEngine = create_engine('postgresql://neondb_owner:zJk7dsFEYl9g@ep-withered-paper-a5kok9au.us-east-2.aws.neon.tech/neondb?sslmode=require')


# Create SQLAlchemy engine
SessionLocal = sessionmaker(largeEngine)
metadata = MetaData()
metadata.reflect(largeEngine)


teams = Table(
    "teams",
    metadata,
    Column("teamID", Integer, primary_key=True, nullable=False),
    Column("name", String(30), nullable=False),
    Column("city", String(100), nullable=False),
    Column("stadium", String(100), nullable=False)
) if "teams" not in metadata.tables else None

players = Table(
    "players",
    metadata,
    Column("playerID", Integer, primary_key=True, nullable=False),
    Column("name", String(100), nullable=False),
    Column("position", String(50), nullable=False),
    Column("age", Integer, nullable=False),
    Column("teamID", Integer, ForeignKey("teams.teamID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
) if "players" not in metadata.tables else None

matches = Table(
    "matches",
    metadata,
    Column("matchID", Integer, primary_key=True, nullable=False),
    Column("homeTeamID", Integer, ForeignKey("teams.teamID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
    Column("awayTeamID", Integer, ForeignKey("teams.teamID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
    Column("matchDate", String(10), nullable=False),
    Column("homeScore", Integer, nullable=False),
    Column("awayScore", Integer, nullable=False),
) if "matches" not in metadata.tables else None


# this prevents it from being created multiple times in the database
if teams and players and matches:
    metadata.create_all(largeEngine)