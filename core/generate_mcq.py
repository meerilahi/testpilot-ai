import json
import os
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai import  TextChunk

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def generate_mcq_by_mistral(difficulty_level: str, chapter_text: str):
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

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()
model = ChatOpenAI(temperature=0.8)
json_schema = {
    "name": "generate_mcq",
    "description": "Generate a multiple choice question with options and correct answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question_text": {"type": "string", "description": "The question"},
            "answer_key": {
                "type": "string",
                "enum": ["A", "B", "C", "D"],
                "description": "The correct option"
            },
            "options": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 4,
                "maxItems": 4,
                "description": "List of four options"
            },
        },
        "required": ["question_text", "answer_key", "options"],
    },
}

structured_model = model.with_structured_output(json_schema)

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
    result = structured_model.invoke(prompt )
    print(f"Open AI Response {result}")
    return result