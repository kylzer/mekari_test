import os
import pandas as pd
import sqlite3

class CSVToSQL:
    def __init__(self, db_path):
        self.db_path = db_path  
    
    def create_db(self):
        """Create SQLite DB"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
    
    def get_db_tables(self):
        """Get all tables"""
        if not os.path.exists(self.db_path):
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            print(f"Error getting tables: {e}")
            return []
    
    def get_table_columns(self, table_name):
        """Get column names for a specific table"""
        if not os.path.exists(self.db_path):
            return []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]
            conn.close()
            return columns
        except Exception as e:
            print(f"Error getting columns: {e}")
            return []
    
    def create_table_from_csv(self, csv_path, table_name):
        """CSV to Table SQL"""
        try:
            if not os.path.exists(self.db_path):
                self.create_db()
            
            df = pd.read_csv(csv_path)
            if df.empty:
                return False, "Empty CSV!"
            
            conn = sqlite3.connect(self.db_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            row_count = len(df)
            conn.close()
            
            return True, f"Table '{table_name}' created with {row_count} rows"
            
        except Exception as e:
            return False, f"Error creating table: {str(e)}"
    
    def append_to_table(self, csv_path, table_name):
        """Append CSV data to existing table with header validation"""
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            
            if df.empty:
                return False, "Empty CSV!"
            
            # Get existing table columns
            existing_columns = self.get_table_columns(table_name)
            csv_columns = df.columns.tolist()
            
            # Check if columns match exactly
            if set(existing_columns) != set(csv_columns):
                missing_in_csv = set(existing_columns) - set(csv_columns)
                extra_in_csv = set(csv_columns) - set(existing_columns)
                
                error_msg = "Data is not match!\n\n"
                if missing_in_csv:
                    error_msg += f"Missing columns in CSV: {', '.join(missing_in_csv)}\n"
                if extra_in_csv:
                    error_msg += f"Extra columns in CSV: {', '.join(extra_in_csv)}"
                
                return False, error_msg
            
            # Reorder CSV columns to match table
            df = df[existing_columns]
            
            # Append to table
            conn = sqlite3.connect(self.db_path)
            df.to_sql(table_name, conn, if_exists='append', index=False)
            
            # Get total row count
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_rows = cursor.fetchone()[0]
            
            conn.close()
            
            return True, f"Successfully added {len(df)} rows to '{table_name}'\nTotal rows: {total_rows}"
            
        except Exception as e:
            return False, f"Error appending to table: {str(e)}"
    
    def get_table_preview(self, table, limit=100):
        if not os.path.exists(self.db_path):
            return "Database does not exist", None
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Rows Total
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                total_rows = cursor.fetchone()[0]

                # Fetch for Preview
                cursor.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))
                rows = cursor.fetchall()

                # Get column names
                columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(rows, columns=columns)

            summary = (
                f"Table: {table}\n"
                f"Total Rows: {total_rows}\n"
            )

            return summary, df

        except Exception as e:
            return f"Error: {e}", None

