from mistralai import Mistral
import os
import json
from dotenv import load_dotenv
from mistralai import  ImageURLChunk, TextChunk
from schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest
from typing import List, Tuple, Optional, Dict, Any

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
def mark_answer(
    answer_text: str,
    answer_key: Optional[str],
    rubric: List[Tuple[str, int]],
    grammer_penalty:str,
    marks: int
    ) -> Dict[str, Any]:

    rubric_str = "\n".join([f"{i+1}. {r[0]}  ({r[1]} marks)" for i, r in enumerate(rubric)])
    prompt = f"""
    You are an expert examiner. Given a student's answer, a model answer (answer key), and evaluation rubrics, you are to evaluate the student’s response.

    Instructions:
    - The answer may also contain a diagram image (if provided).
    - Use the rubrics to assign partial marks for each point.
    - The answer key should guide what points are expected.
    - The diagram_key (if any) shows what the expected diagram should have. Compare it with the student's diagram if provided.

    Answer Key:
    {answer_key or "Not Provided"}

    Rubrics:
    {rubric_str}

    Grammer Penalty:
    {grammer_penalty}

    Student Answer:
    {answer_text}


    Now:
    1. Evaluate each rubric point and assign marks with a short justification.
    2. Return a list in this format:
        [(justification 1, " 1"), ..., (justification N, "marks_awarded_for_point N")]
    3. Deduct marks from total if grammetical and spelling mistakes are present in the answer considering provided penality for grammetical mistakes. If Grammer Penalty is "low" then don't deduct marks.
    3. Return total marks out of {marks}.
    4. Return feedback summarizing what was missing or incorrect in the answer and diagram.

    Return a Python dictionary with keys:
    - 'rubrics': list of tuple (justification for each rubric point, marks_awarded ),
    - 'marks': total marks awarded (int),
    - 'feedback': a summary string.
    """

    message_chunks = [TextChunk(text=prompt)]

    response = client.chat.complete(
        model="pixtral-12b-latest", 
        messages=[
            { "role":"system", "content":"You are an expert exam evaluator."},
            { "role": "user", "content": message_chunks }
        ],
        temperature=0,
        response_format =  {"type": "json_object"}
    )
    result_str = response.choices[0].message.content.strip()
    result = eval(result_str, {"__builtins__": None}, {})
    return result


def mark_answer_sheet(ocr_result , request:MarkSubjectiveAnswerSheetRequest, attempted_qns_mask: Dict[int, bool]):
    answer_keys = {q.question_number : q.answer_key  for q in request.list_of_questions  if attempted_qns_mask[q.question_number]}
    rubrics = {q.question_number : q.rubrics for q in request.list_of_questions if attempted_qns_mask[q.question_number]  if attempted_qns_mask[q.question_number]}
    question_marks = {q.question_number : q.question_marks for q in request.list_of_questions  if attempted_qns_mask[q.question_number]}
    grammer_penalties = {q.question_number : q.grammer_penalty for q in request.list_of_questions if attempted_qns_mask[q.question_number]}
    mark_sheet = {}
    for qn in ocr_result.keys():
        if not attempted_qns_mask[qn]:
            print(f"Skipping question no {qn} as it was not attempted")
            continue
        print(f"Marking question no {qn}")
        marks_dict = mark_answer(answer_text=ocr_result[qn],  answer_key=answer_keys[qn], rubric=rubrics[qn], marks=question_marks[qn], grammer_penalty=grammer_penalties[qn])
        mark_sheet[qn] = marks_dict
    return mark_sheet