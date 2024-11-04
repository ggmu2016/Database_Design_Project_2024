from sqlalchemy import create_engine, Column, String, Integer, CHAR, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('postgresql://schooldb_owner:7clNyHJa9vTY@ep-wild-cell-a80798km.eastus2.azure.neon.tech/schooldb?sslmode=require')


# Create SQLAlchemy engine
SessionLocal = sessionmaker(engine)
metadata = MetaData()
metadata.reflect(engine)

department = Table(
    "department",
    metadata,
    Column("deptCode", CHAR(5), primary_key=True, nullable=False),
    Column("school", String(30), nullable=False),
) if "department" not in metadata.tables else None

major = Table(
    "major",
    metadata,
    Column("studentID", String(30), primary_key=True, nullable=False),
    Column("deptCode", CHAR(5), ForeignKey("department.deptCode", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
) if "major" not in metadata.tables else None

registration = Table(
    "registration",
    metadata,
    Column("studentID", String(30), ForeignKey("major.studentID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False),
    Column("deptCode", CHAR(5), ForeignKey("department.deptCode", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False),
    Column("courseID", Integer, primary_key=True, nullable=False),
) if "registration" not in metadata.tables else None

if registration and major and department:
    metadata.create_all(engine)
