# app.py
"""Application entry point.

Launches the Gradio UI for the document analysis pipeline.
"""
from dotenv import load_dotenv

load_dotenv()

import gradio as gr
from langfuse.langchain import CallbackHandler
from graph import build_graph
from models.schemas import PipelineState
from utils import LOGGER
import os
from utils.cache_cleaner import empty_temp_folder

css = """
footer { display: none !important; visibility: hidden !important; }
.gradio-container { min-height: 0px !important; }
"""

langfuse_handler = CallbackHandler()


def format_report(report) -> str:
    """Format the analysis result for display."""
    if not report:
        return "⚠️ No result found."

    if hasattr(report, "score_a"):
        lines = [
            f"📊 Score A: {report.score_a}/100",
            f"🎯 Score B: {report.score_b}/100",
            f"📝 Score C: {report.score_c}/100",
            "",
            f"🌍 Language / Sections: {report.analysis_content_language_sections}",
            f"🏷️ Title: {report.analysis_content_title}",
            f"👤 Name: {report.analysis_content_name}",
            f"📞 Contact: {report.analysis_content_contact}",
            f"📍 Mobility: {report.analysis_content_geographic_mobility}",
            f"💼 Experience: {report.analysis_content_detailed_experience}",
            f"🔁 Repetitions: {report.analysis_content_repetitions}",
            f"✏️ Spelling Errors: {report.analysis_content_spelling_errors}",
            f"🔑 Keywords: {report.analysis_content_keywords}",
            f"📈 Numeric Results: {report.analysis_content_numeric_results}",
            "",
            f"❌ Missing Items: {', '.join(report.missing_items or [])}",
            "",
            "✅ Corrections:",
            *[f"  - {c}" for c in (report.analysis_content_corrections or [])],
            "",
            "💡 Suggestions:",
            *[f"  - {s}" for s in (report.suggestions or [])],
        ]
        return "\n".join(lines)

    # If report is a business error string
    if isinstance(report, str):
        return f"⚠️ {report}"

    return str(report)


def process_document(doc_file, text_input) -> str:
    # --- Early-return validation ---
    if not doc_file:
        return "⚠️ Please upload a document file (PDF or DOCX)."

    if not text_input or not text_input.strip():
        return "⚠️ Please provide context input."

    try:
        LOGGER.info(f"File received: {doc_file}")

        initial_state = PipelineState(
            input_path=doc_file,
            context=text_input.strip(),
        )
        graph = build_graph()

        final_state = graph.invoke(
            initial_state, config={"callbacks": [langfuse_handler]}
        )

        # Capture errors from nodes
        rag_result = final_state.get("rag_result")
        if isinstance(rag_result, str) and rag_result.startswith("Error"):
            return f"⚠️ {rag_result}"

        report = final_state.get("final_output")

        return format_report(report)

    except ValueError as e:
        # Known errors (unsupported format, invalid path...)
        LOGGER.warning(f"Validation error: {str(e)}")
        return f"⚠️ {str(e)}"
    except Exception as e:
        # Unexpected technical errors
        LOGGER.error(f"Unexpected error in process_document: {str(e)}")
        return f"❌ Unexpected technical error: {str(e)}"


empty_temp_folder()

with gr.Blocks(
    title="Document Analysis Pipeline",
    theme=gr.themes.Soft(),
    css=css,
) as demo:

    with gr.Tabs():

        # ── Tab 1 : Home ──────────────────────────────────────────
        with gr.Tab("🏠 Home"):
            gr.Markdown(
                """
                # 🧩 Document Analysis Pipeline

                Welcome to **Document Analysis Pipeline**, a modular AI-powered document analysis tool.

                ## How it works?
                1. 📄 Upload your document in **PDF** or **DOCX** format
                2. 📝 Paste the **context/query** you want to analyze against
                3. 🚀 Click **Analyze Document**
                4. 📊 Get a detailed report with scores, missing items and suggestions

                ## Privacy
                🔒 Your personal data (name, email, phone) is **anonymized**
                before any analysis. No data is stored after the session.

                ## Supported formats
                - 📄 PDF
                - 📝 DOCX
                """
            )

        # ── Tab 2 : Analyze ──────────────────────────────────────────
        with gr.Tab("🔍 Analyze a Document"):
            gr.Markdown("### 📄 Upload your document and paste the context")
            with gr.Row():
                with gr.Column():
                    file_upload = gr.File(
                        label="Document (PDF or DOCX)",
                        type="filepath",
                        file_types=[".pdf", ".docx"],
                    )
                with gr.Column():
                    text_input = gr.Textbox(
                        lines=10,
                        label="Context / Query",
                        placeholder="Paste the context or query here...",
                    )
            with gr.Row():
                process_button = gr.Button("🚀 Analyze Document", variant="primary")
            with gr.Row():
                result_text = gr.Textbox(
                    lines=25,
                    label="📊 Analysis Result",
                    interactive=False,
                    placeholder="The result will appear here after analysis...",
                )

            process_button.click(
                fn=process_document,
                inputs=[file_upload, text_input],
                outputs=result_text,
                api_visibility="private",
            )

if __name__ == "__main__":
    demo.launch(
        server_port=8080,
        inbrowser=True,
        share=False,
        footer_links=["gradio"],
    )
