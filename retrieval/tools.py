import sqlite3

from pydantic import BaseModel, Field
from langchain.tools import tool

from database import Weaviate

from weaviate import classes
from weaviate.classes.query import Filter, MetadataQuery

from rich.console import Console
console = Console()


# def extract_schema(db_path: str):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT name
#         FROM sqlite_master
#         WHERE type='table'
#         AND name NOT LIKE 'sqlite_%';
#     """)
#     tables = [row[0] for row in cursor.fetchall()]

#     schema = {}

#     for table in tables:
#         cursor.execute(f"PRAGMA table_info({table});")
#         columns = cursor.fetchall()

#         cursor.execute(f"PRAGMA foreign_key_list({table});")
#         fks = cursor.fetchall()

#         schema[table] = {
#             "columns": [
#                 {
#                     "name": col[1],
#                     "type": col[2],
#                     "pk": bool(col[5])
#                 }
#                 for col in columns
#             ],
#             "foreign_keys": [
#                 {
#                     "from": fk[3],
#                     "to_table": fk[2],
#                     "to_column": fk[4]
#                 }
#                 for fk in fks
#             ]
#         }

#     conn.close()
#     return schema

# @tool
# def database_information():

# @tool
# def fraud_database():
#     pass


class FraudDocument(BaseModel):
    question: str = Field(..., description="User Question to retrieve very similar chunk to answer this question")
    collection_name: str = Field(..., description="Needs to filter which collection where's the document stored")
    document_id: str = Field(..., description="Unique ID for a Document to Retrieve as a Knowledge")

@tool(args_schema=FraudDocument)
def fraud_knowledge(question: str = None, collection_name: str = None, document_id: str = None):
    """
    Function to retrieve knowledge from vector database
    Args :
        question        : user question
        collection_name : collection where's the document stored
        document_id     : id to retrieve the document
    """

    chunk_list = []

    vector_conn = Weaviate(collection_name)
    client = vector_conn.client
    with client as client:
        if client.collections.exists(collection_name):
            console.log(f'Successfully connected to collection: {collection_name}')
            collection = client.collections.get(collection_name)
            try:
                response = collection.query.hybrid(
                    query=question,
                    filters=classes.query.Filter.by_property("document_id").contains_any([document_id]),
                    return_metadata=MetadataQuery(distance=True, score=True, explain_score=True),
                    limit=5
                )
                if hasattr(response, 'objects') and response.objects:
                    console.log(f'Found existing objects with document_id: {document_id}')
                    for result in response.objects:
                        chunk_list.append(result.properties.get("page_content", ""))
                    console.log(f"Chunk List :\n{chunk_list}")
                    return chunk_list
                else:
                    console.log(f'No existing objects found with document_id: {document_id}')
                    return f"No existing objects found with document_id: {document_id}"
                
            except Exception as e:
                console.log(f"Error during operation: {str(e)}")
                return "Error during retrieving from weaviate"
        else:
            console.log(f"Collection {collection_name} does not exist")
            return f"Collection named {collection_name} does not exist"
