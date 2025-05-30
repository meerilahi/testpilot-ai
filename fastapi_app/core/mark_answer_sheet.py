from mistralai import Mistral
import os
import json
from dotenv import load_dotenv
from mistralai import  ImageURLChunk, TextChunk
from fastapi_app.schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest
from typing import List, Tuple, Optional, Dict, Any

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
def mark_answer(
    answer_text: str,
    diagram_image: Optional[str],
    answer_key: Optional[str],
    diagram_key: Optional[str],
    rubric: List[Tuple[int, str]],
    grammer_penalty:str,
    marks: int
    ) -> Dict[str, Any]:

    rubric_str = "\n".join([f"{i+1}. ({r[0]} marks) {r[1]}" for i, r in enumerate(rubric)])
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
        [(marks_awarded_for_point1, "justification 1"), ..., (marks_awarded_for_pointN, "justification N")]
    3. Deduct marks from total if grammetical and spelling mistakes are present in the answer considering provided penality for grammetical mistakes. If Grammer Penalty is "No" then don't deduct marks.
    3. Return total marks out of {marks}.
    4. Return feedback summarizing what was missing or incorrect in the answer and diagram.

    Return a Python dictionary with keys:
    - 'rubrics': list of tuple (marks_awarded, justification for each rubric point),
    - 'marks': total marks awarded (int),
    - 'feedback': a summary string.
    """

    message_chunks = [TextChunk(text=prompt)]

    # def is_valid_base64_image(img: Optional[str]) -> bool:
    #     return bool(img and isinstance(img, str) and img.strip() and img.lower() != "none")

    # if is_valid_base64_image(diagram_image):
    #     message_chunks.append(ImageURLChunk(image_url=f"data:image/jpeg;base64,{diagram_image}"))
    # if is_valid_base64_image(diagram_key):
    #     message_chunks.append(ImageURLChunk(image_url=f"data:image/jpeg;base64,{diagram_key}"))

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


def mark_answer_sheet(ocr_result, request:MarkSubjectiveAnswerSheetRequest):
    answer_keys = {q.question_number : q.answer_key  for q in request.list_of_questions}
    diagram_keys = {q.question_number : q.diagram_key  for q in request.list_of_questions}
    rubrics = {q.question_number : q.rubrics for q in request.list_of_questions}
    question_marks = {q.question_number : q.question_marks for q in request.list_of_questions }
    grammer_penalties = {q.question_number : q.grammer_penalty for q in request.list_of_questions}
    mark_sheet = {}
    
    for qn in ocr_result.keys():
        print(f"Marking question no {qn}")
        marks_dict = mark_answer(answer_text=ocr_result[qn]['markdown'], diagram_image=ocr_result[qn]['image'],  answer_key=answer_keys[qn], diagram_key=diagram_keys[qn], rubric=rubrics[qn], marks=question_marks[qn], grammer_penalty=grammer_penalties[qn])
        mark_sheet[qn] = marks_dict
    return mark_sheet