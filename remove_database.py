import os

DB_PATH = "storage/database_storage/database_storage.db"

def delete_test_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Deleted database at: {DB_PATH}")
    else:
        print(f"No database found at: {DB_PATH}")

if __name__ == "__main__":
    delete_test_db()
