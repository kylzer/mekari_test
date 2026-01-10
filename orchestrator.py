import os

from indexing import Indexing
from database import TabularOrchestrator, MetadataRepository
from retrieval import Agent

from langchain_core.messages import AIMessage

from pathlib import Path
import uuid

class DocumentOrchestrator:
    def __init__(self):
        self.file_extracted_folder = "file_extracted/"        
        self.output_extension = ".txt"

        self.db_folder = "database/"
        self.db_name = "data.db"
        self.doc_db_name = "vectorRepo.db"

        self.tabularOrchestrator = TabularOrchestrator(self.db_folder, self.db_name)
        self.metadataRepo = MetadataRepository(self.db_folder, self.doc_db_name)

        os.makedirs(self.db_folder, exist_ok=True)
        os.makedirs(self.file_extracted_folder, exist_ok=True)
        
    def process_pdf(self, file):
        """Handle PDF indexing"""
        preview_text = ""
        if file is None:
            return "No file uploaded! Please check the file...", preview_text
        
        try:
            raw_filename = Path(file).stem        
            indexer = Indexing(file, raw_filename)
            _ = indexer.conversion()

            output_path = f"{self.file_extracted_folder}{raw_filename}{self.output_extension}"
            with open(output_path, "r", encoding="utf-8") as f:
                preview_text = f.read()[:1000]

            try:
                if os.path.getsize(output_path) == 0:
                    return f"Conversion Failed : {raw_filename} -- File is empty!", preview_text
            except FileNotFoundError:
                return f"Conversion Failed : {raw_filename} -- File not created!", preview_text
            
            return f"Conversion Success : {raw_filename} with Max 1000 Lines Preview", preview_text
            
        except Exception as e:
            return f"Conversion Failed : {raw_filename} -- File not created! with error : {str(e)}", preview_text
        
    def chunking_text(self, file):
        """Handle Text Chunking"""
        raw_filename = Path(file).stem   
        file_name = f"{self.file_extracted_folder}{raw_filename}{self.output_extension}"

        status_msg = "Success"

        if "success" not in status_msg.lower() or not os.path.exists(file_name):
            return status_msg 
        
        print("Do Chunking!")
        try:
            indexer = Indexing(filename=file_name)
            status, chunked_text = indexer.chunking()
        except Exception as e:
            return f"Chunking Failed : {raw_filename} -- Docs not Chunked! with error : {str(e)}", []
        return status, chunked_text
    
    def get_collections_from_db(self):
        collections = self.metadataRepo.get_all_collections()
        return ["+ Create New Collection"] + collections
    
    def get_documents_by_collection(self, collection_name):
        return self.metadataRepo.get_documents_by_collection(collection_name)
    
    def upserting_docs(self, status_msg, file, chunked_docs, collection):
        "Handle Upserting to Weaviate"
        raw_filename = Path(file).stem 
        if "success" not in status_msg.lower():
            return status_msg 
        
        if not collection or collection.strip() == "":
            return "Please enter collection name..."
        
        try:
            print("Do Upserting")
            doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, raw_filename))
            indexer = Indexing(raw_filename=raw_filename)
            status = indexer.upserting(doc_id, chunked_docs, collection)
            self.metadataRepo.store_document_metadata(
                collection_name=collection,
                filename=raw_filename,
                doc_id=doc_id,
                status="indexed"
            )
        except Exception as e:
            self.metadataRepo.store_document_metadata(
                collection_name=collection,
                filename=raw_filename,
                doc_id=doc_id,
                status="failed"
            )

            status =  f"Error while Upserting : {str(e)}"

        return status
    
    def process_csv(self, action, file=None, selected_table=None, new_table_name=None, limit=10):
        "Handle CSV Storing"
        if action == "get":
            return self.tabularOrchestrator.get_table_choices()
        elif action == "refresh":
            return self.tabularOrchestrator.refresh_data_view(selected_table, limit)
        elif action == "store":
            return self.tabularOrchestrator.store_csv(file, selected_table, new_table_name, limit)
 
    def retrieve_document(self, query, collection_name, doc_id):
        """Handle document retrieval"""
        if not query:
            return "Please enter the question..."
        
        try:
            agent = Agent(query, collection_name, doc_id)
            agent_model = agent.agent_initiate()
            messages = agent.create_messages()
            response = agent_model.invoke({"messages":messages})

            response_messages = response.get('messages', [])
            ai_message = None
            for msg in reversed(response_messages):
                if hasattr(msg, 'content') and isinstance(msg, AIMessage):
                    ai_message = msg.content
                    break

            return ai_message
        except Exception as e:
            return f"Retrieval Unsucessful with Error: {str(e)}"
        
       
