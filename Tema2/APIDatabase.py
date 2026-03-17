import sqlite3

def get_connection():
    conn = sqlite3.connect('clients.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY NOT NULL,
    status TEXT NOT NULL,
    name TEXT NOT NULL,
    emailAddress TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def get_clients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_client_id(id_client):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM clients WHERE id = ?""",(id_client,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_client_name(id_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM clients WHERE name = ?""",(id_name,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_client(client):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO clients (id, status, name, emailAddress) VALUES (?, ?, ?, ?)
    """, (client['id'], client['status'], client['name'], client['emailAddress']))
    conn.commit()
    conn.close()

def update_client(id_client, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE clients SET status = ?, name = ?, emailAddress = ? WHERE id = ?""",
                   (data['status'], data['name'], data['emailAddress'], id_client))
    conn.commit()
    conn.close()

def delete_client(id_client):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM clients WHERE id = ?""",(id_client,))
    conn.commit()
    conn.close()

