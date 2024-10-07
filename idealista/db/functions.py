import sqlite3

db_path = "data/scrapy_data.db"


def create_table(table_name, columns):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {table_name} ({columns})")
    conn.commit()
    conn.close()


def insert_values(table_name, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columns = ", ".join(data.keys())
    placeholders = ", ".join("?" * len(data))
    values = tuple(data.values())
    cursor.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
    )
    conn.commit()
    conn.close()


def get_house_ids():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT house_id FROM house_location")
    house_ids = cursor.fetchall()
    conn.close()
    return house_ids


def get_garage_ids():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT garage_id FROM garage")
    garage_ids = cursor.fetchall()
    conn.close()
    return garage_ids
