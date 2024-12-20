from sqlalchemy import text, select
from create_tables import engine
from create_large_dataset import largeEngine


# example of query: "SELECT x,y FROM some_table"
def Query2Tuple(query: str, large=False):
    if not large:
        with engine.connect() as conn:
            result = conn.execute(text(query))
    else:
        with largeEngine.connect() as conn:
            result = conn.execute(text(query))
    result_dict = result.mappings().all()
    return result_dict

def Query2TupleLarge(query: str):
    with largeEngine.connect() as conn:
        result = conn.execute(text(query))
        result_dict = result.mappings().all() # python list of dictionaries
    return result_dict

