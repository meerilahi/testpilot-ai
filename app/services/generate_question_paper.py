from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse,QuestionRequest, QuestionResponse
from mistralai import Mistral
from mistralai import  TextChunk
from PyPDF2 import PdfReader
from typing import List
import json
import os
from dotenv import load_dotenv


load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def extract_text_from_pages(pdf_stream, start_page: int, end_page: int) -> str:
    reader = PdfReader(pdf_stream)
    text = ""
    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            text += reader.pages[i].extract_text() or ""
    return text


def generate_questions_from_chapter_text(
    list_of_questions: List[QuestionRequest],
    chapter_text: str
) -> List[QuestionResponse]:
    generated_questions = []

    for question in list_of_questions:
        q_type_lower = question.q_type.lower()

        if q_type_lower == "mcq":
            prompt = (
                f"You are an AI teacher assistant. Based on the following book chapter text, "
                f"generate a **Multiple Choice Question (MCQ)** with the following constraints:\n"
                f"- Difficulty level: {question.difficulty_level}\n"
                f"- Four pptions with one correct option\n\n"
                f"Chapter Text:\n{chapter_text}\n\n"
                f"Return a JSON object with these fields:\n"
                f"- question_text: the question\n"
                f"- answer_key: the correct option e.g is A, B, C, D\n"
                f"- options: a list of 4 available options (including one correct option and other three wrong options)"
            )
        else:
            prompt = (
                f"You are an AI teacher assistant. Based on the following book chapter text, "
                f"generate a **Subjective Question** of type '{question.q_type}' with the following constraints:\n"
                f"- Difficulty level: {question.difficulty_level}\n"
                f"- Total marks: {question.marks}\n\n"
                f"Chapter Text:\n{chapter_text}\n\n"
                f"Return a JSON object with these fields:\n"
                f"- question_text: the question\n"
                f"- answer_key: key points or expected answer\n"
                f"- rubrics: a list of dictionaries, each with `marks` and `requirement`"
            )

        response = client.chat.complete(
            model="pixtral-12b-latest",
            messages=[
                {"role": "system", "content": "You are an AI teacher assistant."},
                {"role": "user", "content": [TextChunk(text=prompt)]}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        try:
            output_json = json.loads(response.choices[0].message.content)
        except Exception as e:
            raise ValueError(f"Invalid response format from Mistral: {e}")

        question_text = str(output_json.get("question_text", ""))
        answer_key = str(output_json.get("answer_key", ""))
        options = output_json.get("options", []) if q_type_lower == "mcq" else []
        rubrics = []

        if q_type_lower != "mcq":
            raw_rubrics = output_json.get("rubrics", [])
            rubrics = [(item["marks"], item["requirement"]) for item in raw_rubrics if isinstance(item, dict)]


        generated_questions.append(QuestionResponse(
            q_no=question.q_no,
            q_type=question.q_type,
            chapter_no=question.chapter_no,
            difficulty_level=question.difficulty_level,
            marks=question.marks,
            question_text=question_text,
            answer_key=answer_key,
            options=options,
            rubrics=rubrics
        ))

    return generated_questions


def generate_question_paper_service(request: GenerateQuestionPaperRequest, book_stream) -> GenerateQuestionPaperResponse:
    all_generated_questions: List[QuestionResponse] = []
    print("Generating Question Paper",flush=True)
    for chapter_no, page_range in request.chapter_pages_dict.items():
        
        chapter_questions = [q for q in request.question_list if q.chapter_no == chapter_no]

        if not chapter_questions:
            continue 
        book_stream.seek(0)
        chapter_text = extract_text_from_pages(book_stream, page_range[0], page_range[1])
        questions =  generate_questions_from_chapter_text(chapter_questions, chapter_text)
        print(f"Questions Generated from chapter {chapter_no}")
        all_generated_questions.extend(questions)
    sorted_questions = sorted(all_generated_questions, key=lambda q: q.q_no)
    print("Question Paper Generated")
    return GenerateQuestionPaperResponse(list_of_question=sorted_questions)