import re
from src.db_session import get_session
import duckdb

focus_data = get_session()


def query_database(
        query: str,
) -> str:
    """
    Execute a SQL query against the table called focus_data.
    Parameters:
        query (str): SQL query string to execute.
    Returns:
        str: json string representation of the query result.
    """
    print("querying database")
    print(query)
    query = query.strip().rstrip(';')
    query = re.sub(r"^```sql\s*|```$", "", query.strip()).strip()
    df = duckdb.query(query).df()
    return df.to_json()