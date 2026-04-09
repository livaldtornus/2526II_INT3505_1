
import sqlite3
import time
import random
import string

DB_NAME = "benchmark_1m.db"
TABLE_NAME = "records"
RECORD_COUNT = 1_000_000

def generate_random_string(length=20):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def setup_db():
    print(f"Creating {DB_NAME} and table '{TABLE_NAME}'...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cursor.execute(f"CREATE TABLE {TABLE_NAME} (id INTEGER PRIMARY KEY, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def populate_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"Generating and inserting {RECORD_COUNT} records (This may take a moment)...")
    
    # Use batch insert for performance
    batch_size = 50000
    for i in range(0, RECORD_COUNT, batch_size):
        records = [(None, generate_random_string(50)) for _ in range(batch_size)]
        cursor.executemany(f"INSERT INTO {TABLE_NAME} (id, content) VALUES (?, ?)", records)
        print(f"  Inserted {(i + batch_size)} / {RECORD_COUNT}...")
    
    conn.commit()
    conn.close()
    print("Data population complete.")

def benchmark():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    limit = 10
    # Let's test deep pages: near the end of 1M records
    offset_deep = 900_000
    cursor_id = 900_000 # For cursor pagination, we start after this ID
    
    print("\n" + "="*50)
    print(f"BENCHMARK: Deep Pagination Comparison (Limit={limit}, Near Row 900K)")
    print("="*50)

    # 1. OFFSET PAGINATION (Deep)
    print(f"Running OFFSET query: SELECT * FROM {TABLE_NAME} LIMIT {limit} OFFSET {offset_deep}...")
    start_time = time.time()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT ? OFFSET ?", (limit, offset_deep))
    results_offset = cursor.fetchall()
    offset_duration = (time.time() - start_time) * 1000 # in ms
    print(f"  Result count: {len(results_offset)}")
    print(f"  Time taken: {offset_duration:.4f} ms")

    # 2. CURSOR PAGINATION (Deep)
    print(f"Running CURSOR query: SELECT * FROM {TABLE_NAME} WHERE id > ? LIMIT ?...")
    # This requires an index on 'id', which SQLite provides by default for PRIMARY KEY
    start_time = time.time()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id > ? LIMIT ?", (cursor_id, limit))
    results_cursor = cursor.fetchall()
    cursor_duration = (time.time() - start_time) * 1000 # in ms
    print(f"  Result count: {len(results_cursor)}")
    print(f"  Time taken: {cursor_duration:.4f} ms")

    print("\n" + "="*50)
    print("SUMMARY RESULTS")
    print("="*50)
    print(f"Offset Pagination: {offset_duration:.4f} ms")
    print(f"Cursor Pagination: {cursor_duration:.4f} ms")
    improvement = offset_duration / cursor_duration if cursor_duration > 0 else 0
    print(f"Cursor Pagination is ~{improvement:.2f}x faster for deep pages!")
    print("="*50)
    
    conn.close()

if __name__ == "__main__":
    setup_db()
    populate_data()
    benchmark()
