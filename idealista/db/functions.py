import sqlite3

def get_house_ids():
    conn = sqlite3.connect('data/scrapy_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT house_id FROM house_location")
    house_ids = cursor.fetchall()
    conn.close()
    return house_ids