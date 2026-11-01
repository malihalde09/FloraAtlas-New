import sqlite3

DB_PATH = "floraatlas.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant (
            plant_id TEXT PRIMARY KEY,
            plant_name TEXT NOT NULL,
            scientific_name TEXT,
            kingdom TEXT,
            family TEXT,
            species TEXT,
            category TEXT,
            description TEXT,
            medicinal_uses TEXT,
            environmental_benefits TEXT,
            image_path TEXT,
            qr_code_id TEXT UNIQUE,
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('SELECT * FROM admin WHERE username = ?', ('admin',))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', ('admin', 'admin123'))
    conn.commit()
    conn.close()

def add_plant(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO plant (plant_id, plant_name, scientific_name, kingdom, family, species, category, description, medicinal_uses, environmental_benefits, image_path, qr_code_id, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['plant_id'], data['plant_name'], data['scientific_name'], data['kingdom'], data['family'], data['species'], data['category'], data['description'], data['medicinal_uses'], data['environmental_benefits'], data['image_path'], data['qr_code_id'], data['latitude'], data['longitude']))
        conn.commit()
        return True, "Plant added successfully!"
    except sqlite3.IntegrityError:
        return False, "Plant ID or QR Code ID already exists!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_all_plants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plant ORDER BY plant_name')
    plants = cursor.fetchall()
    conn.close()
    return plants

def get_plant_by_id(plant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plant WHERE plant_id = ?', (plant_id,))
    plant = cursor.fetchone()
    conn.close()
    return plant

def get_plant_by_qr(qr_code_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plant WHERE qr_code_id = ?', (qr_code_id,))
    plant = cursor.fetchone()
    conn.close()
    return plant

def update_plant(plant_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE plant SET plant_name=?, scientific_name=?, kingdom=?, family=?, species=?, category=?, description=?, medicinal_uses=?, environmental_benefits=?, qr_code_id=?, latitude=?, longitude=?, updated_at=CURRENT_TIMESTAMP
            WHERE plant_id=?
        ''', (data['plant_name'], data['scientific_name'], data['kingdom'], data['family'], data['species'], data['category'], data['description'], data['medicinal_uses'], data['environmental_benefits'], data['qr_code_id'], data['latitude'], data['longitude'], plant_id))
        conn.commit()
        return True, "Plant updated successfully!"
    except sqlite3.IntegrityError:
        return False, "QR Code ID already exists for another plant!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def delete_plant(plant_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM plant WHERE plant_id = ?', (plant_id,))
        conn.commit()
        return True, "Plant deleted successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def search_plants(term, category=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM plant WHERE (plant_name LIKE ? OR scientific_name LIKE ? OR description LIKE ?)"
    params = [f'%{term}%', f'%{term}%', f'%{term}%']
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY plant_name"
    cursor.execute(query, params)
    plants = cursor.fetchall()
    conn.close()
    return plants

def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM plant WHERE category IS NOT NULL AND category != ""')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_total_plants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM plant')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def admin_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    admin = cursor.fetchone()
    conn.close()
    return admin is not None