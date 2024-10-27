from sqlalchemy import create_engine, Column, String, Integer, CHAR, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('postgresql://schooldb_owner:7clNyHJa9vTY@ep-wild-cell-a80798km.eastus2.azure.neon.tech/schooldb?sslmode=require')


# Create SQLAlchemy engine
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

department = Table(
    "department",
    metadata,
    Column("deptCode", CHAR(5), primary_key=True, nullable=False),
    Column("school", String(30), nullable=False),
)

major = Table(
    "major",
    metadata,
    Column("studentID", String(30), primary_key=True, nullable=False),
    Column("deptCode", CHAR(5), ForeignKey("department.deptCode", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
)

registration = Table(
    "registration",
    metadata,
    Column("studentID", String(30), ForeignKey("major.studentID", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False),
    Column("deptCode", CHAR(5), ForeignKey("department.deptCode", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, nullable=False),
    Column("courseID", Integer, primary_key=True, nullable=False),
)

metadata.create_all(engine)
