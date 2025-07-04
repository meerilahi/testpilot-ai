# TestPilot-AI (FastAPI Backend)

This backend powers the AI-based exam system for generating question papers and evaluating scanned answer sheets.

## Features
- ✅ Generate MCQs based on syllabus, chapter, and difficulty
- ✅ Generate subjective questions with answer keys and rubrics
- ✅ Evaluate scanned subjective answer sheets (PDFs)
- ✅ Provide rubric-based feedback for each question

## Missing Features (Planned but not Implemented)
- ❌ Diagram and presentation-based scoring in subjective answers
- ❌ Objective answer sheet evaluation from scanned PDFs
- ❌ Support for Urdu and Arabic languages

## Tech Stack
- FastAPI
- OpenAI/Mistral APIs
- PDF handling libraries (PyMuPDF, PDFMiner, etc.)
- OCR (Mistral)


## How to Run
```bash
uvicorn main:app --reload
```

## Version
Tagged as: `v0.9 - Core AI Features Complete`