import streamlit as st
import requests
import json
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

GENERATE_QUESTIONPAPER_API_URL=os.getenv("GENERATE_QUESTIONPAPER_API_URL")
MARK_ANSWERSHEET_API_URL=os.getenv("MARK_ANSWERSHEET_API_URL")

# -------------------------------
# Utility Functions
# -------------------------------

def generate_question_paper_pdf(response_json) -> bytes:
    buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(buffer.name, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    def draw_line(text, font_size=11, bold=False):
        nonlocal y
        if y < margin:
            c.showPage()
            y = height - margin
        font_name = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font_name, font_size)
        c.drawString(margin, y, text)
        y -= 14

    draw_line("Generated Question Paper", font_size=16, bold=True)
    draw_line("-" * 80)

    for q in response_json["list_of_question"]:
        draw_line(f"Q{q['q_no']}. [{q['q_type']}] Chapter {q['chapter_no']} - {q['difficulty_level']} - {q['marks']} Marks", bold=True)
        draw_line(f"Question: {q['question_text']}")
        draw_line(f"Answer Key: {q['answer_key']}")
        if q["options"]:
            draw_line("Options:")
            for idx, option in enumerate(q["options"], 1):
                draw_line(f"  ({idx}) {option}")
        if q["rubrics"]:
            draw_line("Rubrics:")
            for mark, criterion in q["rubrics"]:
                draw_line(f"  {mark} marks: {criterion}")
        draw_line("-" * 80)

    c.save()
    buffer.seek(0)
    return buffer.read()

def generate_marking_pdf(response_data: dict) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 40, "Subjective Answer Sheet Evaluation Report")
    c.setFont("Helvetica", 12)

    y = height - 80
    for q in response_data.get("list_of_questions", []):
        if y < 100:
            c.showPage()
            y = height - 40
        c.drawString(50, y, f"Question {q['question_number']}")
        y -= 20
        c.drawString(70, y, f"Total Marks Awarded: {q['total_marks']}")
        y -= 20
        c.drawString(70, y, f"Presentation Score: {q['presentation_score']}")
        y -= 20
        c.drawString(70, y, "Rubrics:")
        y -= 20
        for marks, rubric in q["rubrics_marks"]:
            c.drawString(90, y, f"- {rubric}: {marks}")
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 40
        if q.get("feedback"):
            c.drawString(70, y, f"Feedback: {q['feedback']}")
            y -= 30

    y -= 10
    c.drawString(50, y, f"Total Paper Marks: {response_data['total_paper_marks']}")

    c.save()
    buffer.seek(0)
    return buffer

# -------------------------------
# UI Navigation
# -------------------------------

st.sidebar.title("📘 AI Exam System")
page = st.sidebar.selectbox("Select Service", ["📄 Question Paper Generator", "📝 Subjective Sheet Auto-Marking"])

# -------------------------------
# Page 1: Question Paper Generator
# -------------------------------

if page == "📄 Question Paper Generator":
    st.title("📄 AI-Powered Question Paper Generator")
    st.markdown("Upload your book PDF and enter the question configuration below to generate a question paper.")


    uploaded_file = st.file_uploader("📚 Upload Book (PDF)", type=["pdf"])
    chapter_pages_dict = {}
    st.subheader("🧾 Chapter Page Ranges")
    num_chapters = st.number_input("Number of Chapters", min_value=1, value=1)
    for i in range(num_chapters):
        col1, col2, col3 = st.columns(3)
        with col1:
            chapter = st.number_input(f"Chapter #{i+1}", key=f"chap{i}", min_value=1)
        with col2:
            start = st.number_input(f"Start Page", key=f"start{i}", min_value=1)
        with col3:
            end = st.number_input(f"End Page", key=f"end{i}", min_value=1)
        chapter_pages_dict[int(chapter)] = (int(start), int(end))

    st.subheader("🧠 Questions")
    question_list = []
    num_questions = st.number_input("Number of Questions", min_value=1, value=1)
    for i in range(num_questions):
        st.markdown(f"**Question #{i+1}**")
        q_no = i + 1
        q_type = st.selectbox("Type", ["MCQ", "RRQ", "ERQ"], key=f"type{i}")
        chapter_no = st.number_input("Chapter No", key=f"qchap{i}", min_value=1)
        difficulty_level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key=f"diff{i}")
        marks = st.number_input("Marks", key=f"marks{i}", min_value=1)
        question_list.append({
            "q_no": q_no,
            "q_type": q_type,
            "chapter_no": chapter_no,
            "difficulty_level": difficulty_level,
            "marks": marks
        })

    st.subheader("🔘 Choices per Question Type")
    choices_dict = {}
    for qt in ["RRQ", "ERQ"]:
        count = st.number_input(f"{qt} Choices", min_value=1, value=2, key=f"{qt}_choices")
        choices_dict[qt] = int(count)

    if st.button("🚀 Generate Question Paper"):
        if not uploaded_file:
            st.error("Please upload a PDF file.")
        else:
            with st.spinner("Generating..."):
                payload = {
                    "chapter_pages_dict": chapter_pages_dict,
                    "question_list": question_list,
                    "choices_dict": choices_dict
                }

                files = {
                    "file": uploaded_file,
                    "data": (None, json.dumps(payload), "application/json")
                }

                try:
                    res = requests.post(GENERATE_QUESTIONPAPER_API_URL, files=files)
                    if res.status_code == 200:
                        result = res.json()
                        st.session_state["question_paper"] = result
                        pdf_bytes = generate_question_paper_pdf(result)
                        st.session_state["question_paper_pdf"] = pdf_bytes
                        st.success("Question Paper Generated Successfully!")
                    else:
                        st.error(f"Failed to generate paper: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    if "question_paper" in st.session_state:
        result = st.session_state["question_paper"]
        for q in result["list_of_question"]:
            st.markdown(f"### Question #{q['q_no']}")
            st.markdown(f"**Type**: {q['q_type']} | **Chapter**: {q['chapter_no']} | **Difficulty**: {q['difficulty_level']} | **Marks**: {q['marks']}")
            st.markdown(f"**Question Text**: {q['question_text']}")
            st.markdown(f"**Answer Key**: {q['answer_key']}")
            if q.get("options"):
                st.markdown("**Options:**")
                for idx, opt in enumerate(q["options"]):
                    st.markdown(f"- ({idx+1}) {opt}")
            if q.get("rubrics"):
                st.markdown("**Rubrics:**")
                for mark, criterion in q["rubrics"]:
                    st.markdown(f"- {mark} marks: {criterion}")
            st.markdown("---")

        st.download_button("📥 Download JSON", data=json.dumps(result, indent=2),
                           file_name="generated_question_paper.json", mime="application/json")

        if "question_paper_pdf" in st.session_state:
            st.download_button("📥 Download PDF", data=st.session_state["question_paper_pdf"],
                               file_name="generated_question_paper.pdf", mime="application/pdf")


# -------------------------------
# Page 2: Subjective Sheet Auto-Marking
# -------------------------------

elif page == "📝 Subjective Sheet Auto-Marking":
    st.title("📄 Subjective Sheet Auto-Marking (BISEP Style)")

    uploaded_file = st.file_uploader("Upload Answer Sheet (PDF)", type=["pdf"])

    try:
        with open("streamlit_app/sample.json", "r") as f:
            parsed_data = json.load(f)
    except Exception as e:
        st.error(f"Failed to load sample.json: {e}")
        st.stop()

    if st.button("Mark Answer Sheet"):
        if uploaded_file is None:
            try:
                with open("streamlit_app/default_answer_sheet.pdf", "rb") as f:
                    uploaded_file = BytesIO(f.read())
                    uploaded_file.name = "default_answer_sheet.pdf"
            except FileNotFoundError:
                st.error("Please upload a PDF file or ensure default_answer_sheet.pdf exists.")
                st.stop()

        with st.spinner("Marking in progress..."):
            response = requests.post(
                MARK_ANSWERSHEET_API_URL,
                data={"data": json.dumps(parsed_data)},
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )

        if response.status_code == 200:
            response_data = response.json()
            st.session_state["marked_sheet"] = response_data
            st.success("Sheet marked successfully!")

            st.subheader("📊 Marks Breakdown")
            for q in response_data["list_of_questions"]:
                st.markdown(f"### Question {q['question_number']}")
                st.markdown(f"**Total Marks Awarded**: {q['total_marks']}")
                st.markdown(f"**Presentation Score**: {q['presentation_score']}")
                st.markdown("**Rubric Marks:**")
                for marks, rubric in q["rubrics_marks"]:
                    st.markdown(f"- {rubric}: {marks}")
                if q.get("feedback"):
                    st.markdown(f"**Feedback**: {q['feedback']}")
        else:
            st.error(f"API Error [{response.status_code}]: {response.text}")

    if "marked_sheet" in st.session_state:
        response_data = st.session_state["marked_sheet"]
        pdf_bytes = generate_marking_pdf(response_data)
        st.download_button(
            label="Download Marked Sheet PDF",
            data=pdf_bytes,
            file_name="marked_subjective_sheet.pdf",
            mime="application/pdf"
        )
