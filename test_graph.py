# test_graph.py
from dotenv import load_dotenv

load_dotenv()

import traceback
from graph import build_graph
from models.schemas import AnalyzerState

state = AnalyzerState(
    cv_path="D:/AFFAIRES_PERSO/EMPLOI/CV_OLD/ExempleCVConsultants/CV _BLA.docx",
    job_specs="test",
)
try:
    result = build_graph().invoke(state)
    print(result)
except Exception as e:
    traceback.print_exc()
