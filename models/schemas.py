# models/schemas.py
from typing import TypedDict, List, Optional, Any
from pydantic import BaseModel


class AnalysisResult(BaseModel):
    """Structured output schema for the analysis pipeline."""

    analysis_content_language_sections: Optional[str] = None
    analysis_content_title: Optional[str] = None
    analysis_content_name: Optional[str] = None
    analysis_content_contact: Optional[str] = None
    analysis_content_geographic_mobility: Optional[str] = None
    analysis_content_detailed_experience: Optional[str] = None
    analysis_content_repetitions: Optional[str] = None
    analysis_content_spelling_errors: Optional[str] = None
    analysis_content_corrections: Optional[List[str]] = None
    analysis_content_keywords: Optional[str] = None
    analysis_content_numeric_results: Optional[str] = None
    score_a: Optional[int] = None
    score_b: Optional[int] = None
    score_c: Optional[int] = None
    missing_items: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None


class PipelineState(TypedDict):
    """State schema for the LangGraph pipeline."""

    input_path: str
    context: str
    document_content: str
    context_text: str
    rag_result: Any
    final_output: Any
