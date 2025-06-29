import json
import os
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai import  TextChunk
load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def generate_mcq(difficulty_level: str, chapter_text: str):
    prompt = (
        f"You are an AI teacher assistant. Based on the following book chapter text, "
        f"generate a **Multiple Choice Question (MCQ)** with the following constraints:\n"
        f"- Difficulty level: {difficulty_level}\n"
        f"- Four options with one correct option\n\n"
        f"Chapter Text:\n{chapter_text}\n\n"
        f"Return a JSON object with these fields:\n"
        f"- question_text: the question\n"
        f"- answer_key: the correct option e.g is A, B, C, D\n"
        f"- options: a list of 4 available options (including one correct option and other three wrong options)"
    )

    response = client.chat.complete(
        model="pixtral-12b-latest",
        messages=[
            {"role": "system", "content": "You are an AI teacher assistant."},
            {"role": "user", "content": [TextChunk(text=prompt)]}
        ],
        temperature=1,
        response_format={"type": "json_object"}
    )

    output_json = json.loads(response.choices[0].message.content)
    return output_json