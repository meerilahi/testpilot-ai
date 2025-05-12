from fastapi import FastAPI, APIRouter, HTTPException
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / "models"))
from module.schemas import NotesInfoList, PaperFormat, PaperResponse
from services import get_notes_info, generate_paper

router = APIRouter()

@router.get("/notes-info", response_model=NotesInfoList)
def fetch_notes_info():
    return get_notes_info()

@router.post("/generate-paper", response_model=PaperResponse)
def generate_exam_paper(paper_format: PaperFormat):
    paper = generate_paper(paper_format)
    if not paper:
        raise HTTPException(status_code=400, detail="Paper generation failed.")
    return paper

