from sqlalchemy import text, select
from create_tables import engine


# example of query: "SELECT x,y FROM some_table"
def Query2Tuple(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
    return result

# function that creates a different table/or create view

def main():
    Query2Tuple("select ")
