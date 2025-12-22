from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd

@dataclass
class TabularStoringResponse:
    """
    TabularOrchestrator Response Model
    """
    status: str
    dropdown: Any
    summary: str
    preview: pd.DataFrame

@dataclass
class VectorInput:
    """
    Document Vectorized Store
    """
    document_id: str
    page_content: str
    metadata: Dict

@dataclass
class VectorMetadata:
    """
    Metadata for Vectorized Store
    """
    keywords: list
    summary: str
    filename: str

class Summary(BaseModel):
    summary: str = Field(description="Combination of Summary and Conclusion of the Content")

class Keywords(BaseModel):
    keywords: list = Field(description="Specific unique keywords")
    entities: list = Field(description="Mentioned entity such as, people, organization, building, etc")
    questions: list = Field(description="Hypothetical Questions to help RAG retrieval")