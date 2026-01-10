from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from utils import langchainModel
from retrieval.prompt import SYSTEM_PROMPT
from retrieval.tools import fraud_knowledge, database_information, fraud_database

from rich.console import Console
console = Console()

class Agent:
    def __init__(self, query, collection_name, doc_id):
        self.model = langchainModel()
        self.query = query
        self.collection_name = collection_name
        self.document_id = doc_id

    def agent_initiate(self):
        tools = [fraud_knowledge, database_information, fraud_database]
        agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            debug=True
        )
        console.log("Agent Created!")
        return agent
    
    def create_messages(self):
        messages = f"""
        Document ID : {self.document_id}
        Collection Name : {self.collection_name}
        
        Question : {[HumanMessage(content=self.query)]}"""
        print(messages)
        return messages