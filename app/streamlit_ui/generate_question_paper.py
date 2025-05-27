import streamlit as st
import requests
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import tempfile

def generate_pdf(response_json) -> bytes:
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


st.title("📄 AI-Powered Question Paper Generator")

st.markdown("Upload your book PDF and enter the question configuration below to generate a question paper.")

# Backend URL (update this if hosted elsewhere)
API_URL = "http://localhost:8000/generate_question_paper"

# Upload book file
uploaded_file = st.file_uploader("📚 Upload Book (PDF)", type=["pdf"])

# Chapter pages input
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

# Question list
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

# Choices dict
st.subheader("🔘 Choices per Question Type")
choices_dict = {}
for qt in ["RRQ", "ERQ"]:
    count = st.number_input(f"{qt} Choices", min_value=1, value=2, key=f"{qt}_choices")
    choices_dict[qt] = int(count)

# Submit
if st.button("🚀 Generate Question Paper"):
    if not uploaded_file:
        st.error("Please upload a PDF file.")
    else:
        with st.spinner("Generating..."):
            # Prepare the request
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
                res = requests.post(API_URL, files=files)
                # Inside try block after successful response
                if res.status_code == 200:
                    result = res.json()
                    # Save to session state
                    st.session_state["question_paper"] = result
                    # Save locally
                    with open("generated_question_paper.json", "w") as f:
                        json.dump(result, f, indent=2)
                    st.success("Question Paper Generated Successfully!")
                    # Generate PDF and store it in session state
                    pdf_bytes = generate_pdf(result)
                    st.session_state["question_paper_pdf"] = pdf_bytes
                else:
                    st.error(f"Failed to generate paper: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# If a question paper exists in session state, show it
if "question_paper" in st.session_state:
    result = st.session_state["question_paper"]

    # Download button


    # Display questions
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
    
    # PDF download
    if "question_paper_pdf" in st.session_state:
        st.download_button("📥 Download PDF", data=st.session_state["question_paper_pdf"],
                        file_name="generated_question_paper.pdf", mime="application/pdf")