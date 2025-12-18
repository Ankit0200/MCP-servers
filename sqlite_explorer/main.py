from fastmcp import FastMCP
mcp=FastMCP("sqlite-explorer")
# import shutil,psutil

# @mcp.resource("system://stats")
# def get_stats():
    
#     cpu = psutil.cpu_percent()
    
#     # Get Disk Usage (Standard Python library)
#     total, used, free = shutil.disk_usage("/")
#     return f"CPU: {cpu}% | Disk Free: {free // (2**30)} GB"

# @mcp.resource("system://greet/{name}")
# def greet(name: str):
#     return "Hello " + name


# if __name__ == "__main__":
#     mcp.run()


# A safe architecture project
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "my_app.db")
def setup_dummy_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)")
    conn.commit()
    conn.close()

setup_dummy_db()

@mcp.resource("database://schema")
def read_schema() -> str:
    "returns the database schema for llm to study"
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    schema_text = "DATABASE SCHEMA:\n"

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        schema_text += f"\nTable: {table_name}\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            schema_text += f"  Column: {column[1]}, Type: {column[2]}\n"

    conn.close()
    return schema_text

@mcp.tool()
def read_table(table_name: str) -> str:
    "reads all rows from a given table"
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        result = f"Rows in table {table_name}:\n"
        for row in rows:
            result += str(row) + "\n"
    except sqlite3.Error as e:
        result = f"An error occurred: {e}"
    conn.close()
    return result

@mcp.tool("run_query")
def run_query(query: str) -> str:
    "executes a given SQL query and returns the results." 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = "Query Results:\n"
        for row in rows:
            result += str(row) + "\n"
    except sqlite3.Error as e:
        result = f"An error occurred: {e}"
    conn.close()
    return result





if __name__ == "__main__":
    mcp.run()
