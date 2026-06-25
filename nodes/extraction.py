# nodes/extraction.py
"""Document extraction and sanitization node.

Handles text extraction from PDF/DOCX files and applies security scanners
for PII anonymization and prompt injection detection.
"""
from utils import LOGGER
import fitz
from docx import Document
from llm_guard import scan_prompt
from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize, PromptInjection
from utils.preprocessing import collapse_spaced_letters


_vault = Vault()
_scanners = [
    Anonymize(
        _vault,
        entity_types=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "URL"],
        use_onnx=False,
    ),
    PromptInjection(use_onnx=False),
]


def extract_text(path: str) -> str:
    """
    Extracts text from a file based on its file extension.

    Supported formats:
        - PDF (.pdf): Uses PyMuPDF (fitz) to extract text from all pages
        - DOCX (.docx): Uses python-docx to extract text from paragraphs

    Args:
        path: File path to the document to be processed

    Returns:
        str: Extracted text content from the file

    Raises:
        ValueError: If the file format is not supported (neither .pdf nor .docx)
    """
    if path.endswith(".pdf"):
        LOGGER.info("Extraction node: Processing PDF...")
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    elif path.endswith(".docx"):
        LOGGER.info("Extraction node: Processing DOCX...")
        return "\n".join(p.text for p in Document(path).paragraphs).replace("\xa0", " ")
    elif path.endswith(".doc"):
        LOGGER.error("Format .doc not supported, convert to .docx")
        raise ValueError(
            "Format .doc not supported. Please convert your file to .docx."
        )
    raise ValueError(f"Unsupported format: {path}")


def sanitize(text: str, scanners: list) -> tuple[str, bool]:
    """
    Sanitizes text by collapsing spaced letters and scanning for potential risks.

    Process steps:
        1. Collapse spaced-out uppercase letters
        2. Scan text using provided scanners (e.g., PII detection, prompt injection)

    Args:
        text: Raw text to be sanitized
        scanners: List of llm_guard scanners to apply to the text

    Returns:
        tuple[str, bool]:
            - First element: Sanitized text with PII/risks removed
            - Second element: Boolean indicating if the text was valid (no risks detected)

    Note:
        This function is used for document and context input validation.
    """
    text = collapse_spaced_letters(text)
    sanitized, is_valid, _ = scan_prompt(scanners, text)
    return sanitized, is_valid


def extraction_node(state: dict) -> dict:
    """
    Extraction node: Loads and validates document content and context input from the state.
    """
    LOGGER.info("Extraction node: Loading and validating data...")

    input_path = state.get("input_path", "")
    context = state.get("context", "")

    if not input_path:
        LOGGER.error("input_path is empty")
        return {"rag_result": "Error: missing file path."}

    try:
        text = extract_text(input_path)
    except ValueError as e:
        LOGGER.error(str(e))
        return {"rag_result": str(e)}

    sanitized_doc, doc_valid = sanitize(text, _scanners)
    if not doc_valid:
        LOGGER.error("Block! Attempted injection or risky content detected")
        return {"rag_result": "Error: invalid document content."}

    sanitized_context = ""
    if context:
        sanitized_context, context_valid = sanitize(context, _scanners)
        if not context_valid:
            LOGGER.error("Block! Attempted injection or risky content in context input")
            return {"rag_result": "Error: invalid context input."}
    else:
        LOGGER.warning("Context input is empty")

    return {"document_content": sanitized_doc, "context_text": sanitized_context}
