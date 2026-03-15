import sqlite3

def check_db():
    conn = sqlite3.connect("data/smartstore.db")
    cursor = conn.cursor()
    
    tables = ["products", "orders", "inquiries"]
    
    for table in tables:
        print(f"\n--- {table.capitalize()} Table ---")
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            # 필드명 가져오기
            columns = [description[0] for description in cursor.description]
            print(f"Columns: {columns}")
            for row in rows:
                print(row)
            print(f"Total rows: {len(rows)}")
        except Exception as e:
            print(f"Error reading {table}: {e}")
            
    conn.close()

if __name__ == "__main__":
    check_db()
