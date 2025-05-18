from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

load_dotenv()


async def generate_question_paper_service(paperRequest: GenerateQuestionPaperRequest) -> GenerateQuestionPaperResponse:
    
    chat = ChatOpenAI()
    parser = PydanticOutputParser(pydantic_object=GenerateQuestionPaperResponse)
    prompt_template = PromptTemplate(
        template=(
        "You are an expert exam generator. Create a question paper from following syllabus text based for the following criteria:\n"
        "Syllabus_text: {{syllabus_text}}\n"
        "Difficulty: {{difficulty_level}}\n"
        "Number of MCQs Questions: {{no_of_mcq}}\n"
        "Number of Short Questions: {{no_of_short_questions}}\n"
        "Number of Long Questions: {{no_of_long_questions}}\n"
        "{FORMAT_INSTRUCTIONS}"
        ),
        input_variables=[
            "syllabus_text",
            "difficulty_level",
            "no_of_mcq",
            "no_of_short_questions",
            "no_of_long_questions",
        ],
        partial_variables={
            "FORMAT_INSTRUCTIONS": parser.get_format_instructions()
        },
    )

    chain = prompt_template | chat | parser

    return await chain.ainvoke({
        "syllabus_text": SYLLABUS_TEXT,
        "difficulty_level": paperRequest.difficulty_level,
        "no_of_mcq": paperRequest.no_of_mcq,
        "no_of_short_questions": paperRequest.no_of_short_questions,
        "no_of_long_questions": paperRequest.no_of_long_questions,
    })
