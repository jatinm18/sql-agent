import sqlite3
from langchain.tools import tool
from .database import get_connection, list_tables
from .config import get_model

model = get_model()

@tool
def sql_db_list_tables() -> str:
    """Input is an empty string, output is a comma-separated list of tables in the database."""
    return ", ".join(list_tables())

@tool
def sql_db_schema(table_names: str) -> str:
    """Input is a comma-separated list of tables, output is the schema and sample rows.
    Call sql_db_list_tables first to verify table names exist.
    Example Input: table1, table2"""
    con = get_connection()
    try:
        cursor = con.cursor()
        valid_tables = set(list_tables())
        results = []
        for table in table_names.split(","):
            table = table.strip()
            if table not in valid_tables:
                results.append(f"Error: table {table!r} not found in database")
                continue
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,))
            schema_row = cursor.fetchone()
            if schema_row:
                results.append(schema_row[0])
                quoted = '"' + table.replace('"', '""') + '"'
                cursor.execute(f"SELECT * FROM {quoted} LIMIT 3;")
                rows = cursor.fetchall()
                if rows:
                    cols = [d[0] for d in cursor.description]
                    results.append(
                        f"/*\n3 rows from {table}:\n"
                        + "\t".join(cols) + "\n"
                        + "\n".join("\t".join(str(x) for x in row) for row in rows)
                        + "\n*/"
                    )
        return "\n\n".join(results)
    finally:
        con.close()

@tool
def sql_db_query(query: str) -> str:
    """Execute a correct SQL query and return results.
    If an error is returned, rewrite the query and try again."""
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute(query)
        return str(cursor.fetchall())
    except Exception as e:
        return f"Error: {e}"
    finally:
        con.close()

@tool
def sql_db_query_checker(query: str) -> str:
    """Double-check a SQL query for mistakes before executing it.
    Always call this before sql_db_query."""
    prompt = f"""{query}

Double check the sqlite query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are mistakes, rewrite the query. If not, reproduce the original query.
Output the final SQL query only.

SQL Query: """
    response = model.invoke(prompt)
    return response.text.strip()

tools = [sql_db_list_tables, sql_db_schema, sql_db_query, sql_db_query_checker]