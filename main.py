import gradio as gr

from orchestrator import DocumentOrchestrator
from ui import indexing_ui, sql_ui, retrieval_ui

from dotenv import load_dotenv
load_dotenv()

orchestrator = DocumentOrchestrator()

def create_ui():
    with gr.Blocks(title="RAG + Tabular System", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Indexing & Tabular + Retrieval ")
        
        with gr.Tabs():
            # Indexing
            indexing_ui(orchestrator)
            
            # Tabular
            sql_ui(orchestrator)

            # Retrieval
            retrieval_ui(orchestrator)

    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )