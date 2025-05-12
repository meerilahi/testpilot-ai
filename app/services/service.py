from schemas import NotesInfoList, NotesInfo, PaperGenerationRequest, PaperResponse

NOTES_DB = {
    "note1": {"title": "Physics Notes", "length": 100, "text": "full notes text here..."},
    "note2": {"title": "Math Notes", "length": 80, "text": "full notes text here..."},
}

def get_notes_info() -> NotesInfoList:
    return NotesInfoList(notes=[
        NotesInfo(notes_id=note_id, title=data["title"], length=data["length"])
        for note_id, data in NOTES_DB.items()
    ])

def generate_exam_paper(request: PaperGenerationRequest) -> PaperResponse:
    note = NOTES_DB.get(request.notes_id)
    if not note:
        return PaperResponse(paper_text="Invalid notes ID.")
    
    selected_text = f"(Selected pages: {', '.join(request.page_ranges)})\n{note['text']}"
    
    # Placeholder for LLM call
    generated_paper = f"Generated paper using:\n{selected_text}\nFormat: {request.paper_format}"
    
    return PaperResponse(paper_text=generated_paper)
