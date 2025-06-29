from schemas.generate_question import GenerateQuestionResponse
from mistralai import Mistral
from mistralai import  TextChunk
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def generate_question(
    q_type : str,
    difficulty_level: str,
    marks: int,
    text: str
) -> GenerateQuestionResponse:

    prompt = (
        f"You are an AI teacher assistant. Based on the following book chapter text, "
        f"generate a **Subjective Question**  with the following constraints:\n"
        f"- Answer Length: {q_type}\n"
        f"- Difficulty level: {difficulty_level}\n"
        f"- Total marks: {marks}\n\n"
        f"Chapter Text:\n{text}\n\n"
        f"Return a JSON object with these fields:\n"
        f"- question_text: the question\n"
        f"- answer_key: key points or expected answer\n"
        f"- rubrics: a list of dictionaries, each with `requirement` and `marks`"
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
    rubrics = [(item["requirement"], item["marks"]) for item in raw_rubrics if isinstance(item, dict)]

    return GenerateQuestionResponse(
            question_text=question_text,
            answer_key=answer_key,
            rubrics=rubrics
        )