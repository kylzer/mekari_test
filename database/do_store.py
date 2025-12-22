from database.to_sql import CSVToSQL
from model import TabularStoringResponse

import os
import gradio as gr

class TabularOrchestrator:
    def __init__(self, db_folder, db_name):
        self.db_folder = db_folder 
        self.db_name = db_name     

        self.db_path = f"{db_folder}{db_name}"      
        os.makedirs(db_folder, exist_ok=True)

        self.sql_handler = CSVToSQL(self.db_path)
    
    def response(self, message, table, summary="", preview=None):
        """Modelling response output"""
        r = TabularStoringResponse(message, self.update_dropdown(self.get_table_choices(), table), summary, preview)
        return r.status, r.dropdown, r.summary, r.preview

    def update_dropdown(self, choices, value):
        """Update dropdown list"""
        return gr.update(choices=choices, value=value)
    
    def get_table_choices(self):
        """Get tables dropwdown"""
        if not os.path.exists(self.db_path):
            return ["+ Create New Table"]
        
        tables = self.sql_handler.get_db_tables()
        
        if not tables:
            return ["+ Create New Table"]        
        return tables + ["+ Create New Table"]
    
    def store_csv(self, file, selected_table, new_table_name, preview_limit):
        """Store CSV to database"""
        if file is None:
            return self.response("No file uploaded!", selected_table)
        
        try:
            if selected_table == "+ Create New Table":
                if not new_table_name or new_table_name.strip() == "":
                    return self.response("Please provide a table name!", selected_table)
                
                table_name = new_table_name.strip().replace(" ", "_").replace("-", "_")                
                success, message = self.sql_handler.create_table_from_csv(file, table_name)
                
                if not success:
                    return self.response(f"{message}", selected_table)
                                
            else:
                table_name = selected_table
                success, message = self.sql_handler.append_to_table(file, table_name)
                
                if not success:
                    return self.response(f"{message}", selected_table)
            
            summary, preview = self.sql_handler.get_table_preview(table_name, preview_limit)
            return self.response(message, selected_table, summary, preview)
                        
        except Exception as e:
            return self.response(f"Error: {str(e)}", selected_table)
    
    def refresh_data_view(self, table, preview_limit):
        """Refresh showing data"""
        summary, preview = self.sql_handler.get_table_preview(table, preview_limit)
        return summary, preview