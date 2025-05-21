from typing import List, Dict
from pydantic import BaseModel
from typing_extensions import Annotated
from mistralai import Mistral, TextChunk
from dotenv import load_dotenv
import json
import os
from app.schemas.mark_answer_sheet import MarkAnswerSheetRequest, MappedAnswers

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def map_answers(markdown: str, request: MarkAnswerSheetRequest) -> MappedAnswers:

    sectionA_questions = [{"number": q.number, "question": q.question, "options": q.options} for q in request.sectionA]
    sectionB_questions = [{"number": q.number, "question": q.question} for q in request.sectionB]
    sectionC_questions = [{"number": q.number, "question": q.question} for q in request.sectionC]

    prompt = f"""
    You are an intelligent assistant. You will be given:
    1. A markdown document containing student answers.
    2. A structured list of questions for three sections: A (MCQs), B (Short Questions), and C (Long Questions).
    Your task is to map each student answer to its corresponding question number. Return your output as three lists (sectionA, sectionB, sectionC), where each list contains dictionaries with question number as the key and student answer as the value.
    If no answer is found, use an empty string as the answer.
    Markdown (student response):
    ---
    {markdown}
    ---
    Section A (MCQs):
    {json.dumps(sectionA_questions, indent=2)}

    Section B (Short Questions):
    {json.dumps(sectionB_questions, indent=2)}

    Section C (Long Questions):
    {json.dumps(sectionC_questions, indent=2)}

    Respond in this exact JSON format:
    {{
    "sectionA": [{{ "1": "Answer text" }}, ...],
    "sectionB": [{{ "2": "Answer text" }}, ...],
    "sectionC": [{{ "3": "Answer text" }}, ...]
    }}
        """
    
    chat_response = client.chat.parse(
        model="pixtral-12b-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    prompt
                ],
            },
        ],
        response_format=MappedAnswers,
        temperature=0
    )

    print(chat_response.model_dump_json())

    return None
    

    
