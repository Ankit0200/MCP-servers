import sqlite3
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from fastmcp import FastMCP

# 1. Initialize FastMCP (Standard Mode)
# IMPORTANT: This name must match what you put in your OpenAI client config
mcp = FastMCP("data_visualizer_mcp")

# --- Setup Paths & Database ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data_visualizer.db")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Create dummy tables if they don't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT, category TEXT, price REAL, cost REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            product_id INTEGER, date TEXT, quantity INTEGER, region TEXT
        )
    """)
    conn.commit()
    conn.close()

setup_database()

# --- Define Tools using @mcp.tool ---

@mcp.tool()
def read_table(table_name: str) -> str:
    """Read all rows from a specific table."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        return "\n".join(map(str, rows)) if rows else "Table is empty."
    except Exception as e:
        return f"Error reading table: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def run_query(query: str) -> str:
    """Run a raw SQL query on the database."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        return "\n".join(map(str, rows))
    except Exception as e:
        return f"Query failed: {str(e)}"
    finally:
        conn.close()

@mcp.tool()
def generate_chart(query: str, chart_type: str, title: str) -> str:
    """Generate a chart (bar, line, pie) from a SQL query and return the image path."""
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return "Query returned no data, cannot generate chart."

        plt.figure(figsize=(10, 6))
        
        # Assumption: 1st column = labels, 2nd column = values
        labels = df.iloc[:, 0]
        values = df.iloc[:, 1]

        if chart_type == "bar":
            plt.bar(labels, values)
        elif chart_type == "line":
            plt.plot(labels, values)
        elif chart_type == "pie":
            plt.pie(values, labels=labels)
        else:
            return "Invalid chart_type. Use 'bar', 'line', or 'pie'."

        plt.title(title)
        
        # Save chart
        filename = f"chart_{int(time.time())}.png"
        path = os.path.join(CHARTS_DIR, filename)
        plt.savefig(path)
        plt.close()
        
        return f"Chart saved successfully at: {path}"
    except Exception as e:
        return f"Error generating chart: {str(e)}"
    finally:
        conn.close()

# --- Run the Server ---
if __name__ == "__main__":
    # Use transport="sse" for HTTP connectivity (required for OpenAI clients accessing via URL)
    mcp.run(transport="sse")