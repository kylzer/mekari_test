import sqlite3
import os

class MetadataRepository:
    def __init__(self, db_folder, db_name):
        self.db_path = os.path.join(db_folder, db_name)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_name TEXT NOT NULL,
                doc_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    
    def store_document_metadata(self, collection_name, filename, doc_id, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO documents (collection_name, doc_id, filename, status)
            VALUES (?, ?, ?, ?)
        """, (collection_name, doc_id, filename, status))
        conn.commit()
        conn.close()
    
    def get_all_collections(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT collection_name FROM documents ORDER BY collection_name')
        collections = [row[0] for row in cursor.fetchall()]
        conn.close()
        return collections
    
    def get_documents_by_collection(self, collection_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT doc_id, filename 
            FROM documents 
            WHERE collection_name = ? 
            ORDER BY filename
        ''', (collection_name,))
        documents = cursor.fetchall()
        conn.close()
        return documents