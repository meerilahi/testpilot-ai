from fastapi_app.schemas.generate_subjective_questions import QuestionRequest, QuestionResponse
from mistralai import Mistral
from mistralai import  TextChunk
from typing import List
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def generate_rrqs_erqs(
    list_of_questions: List[QuestionRequest],
    chapter_text: str
) -> List[QuestionResponse]:
    generated_questions = []

    for question in list_of_questions:

        prompt = (
            f"You are an AI teacher assistant. Based on the following book chapter text, "
            f"generate a **Subjective Question**  with the following constraints:\n"
            f"- Answer Length: {question.q_type}\n"
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
            temperature=0.6,
            response_format={"type": "json_object"}
        )

        try:
            output_json = json.loads(response.choices[0].message.content)
        except Exception as e:
            raise ValueError(f"Invalid response format from Mistral: {e}")

        question_text = str(output_json.get("question_text", ""))
        answer_key = str(output_json.get("answer_key", ""))
        rubrics = []
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
            rubrics=rubrics
        ))

    return generated_questions