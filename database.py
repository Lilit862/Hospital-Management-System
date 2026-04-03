# database.py — Central database connection
# All other files import from here

import pyodbc

# ============================================================
#  UPDATE THESE TWO LINES WITH YOUR SQL SERVER DETAILS
# ============================================================
SERVER   = r".\SQLEXPRESS"   # e.g. DESKTOP-XYZ\SQLEXPRESS
DATABASE = "HospitalDB"
# ============================================================

def get_connection():
    """Return a live pyodbc connection. Call this in every route."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


def query(sql, params=(), one=False):
    """
    Run a SELECT query.
    Returns a list of dicts, or a single dict if one=True.
    """
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    cols = [col[0] for col in cursor.description]
    if one:
        row = cursor.fetchone()
        conn.close()
        return dict(zip(cols, row)) if row else None
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


def execute(sql, params=()):
    """
    Run INSERT / UPDATE / DELETE and commit.
    Returns the last inserted row ID (if available).
    """
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    # Try to get the new row's ID (for INSERT statements)
    last_id = None
    try:
        cursor.execute("SELECT @@IDENTITY")
        last_id = cursor.fetchone()[0]
    except Exception:
        pass
    conn.commit()
    conn.close()
    return last_id
