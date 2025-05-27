import streamlit as st
import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(response_data: dict) -> BytesIO:
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


st.title("📄 Subjective Sheet Auto-Marking (BISEP Style)")

# Input FastAPI URL
api_url = st.text_input("FastAPI Endpoint URL", "http://localhost:8000/mark_bisep_subjective")

# Upload PDF file
uploaded_file = st.file_uploader("Upload Answer Sheet (PDF)", type=["pdf"])

# Load marking instructions from sample.json
try:
    with open("app/streamlit_ui/sample.json", "r") as f:
        parsed_data = json.load(f)
except Exception as e:
    st.error(f"Failed to load sample.json: {e}")
    st.stop()

# Submit Button
if st.button("Mark Answer Sheet"):

    # If no file uploaded, use default PDF
    if uploaded_file is None:
        try:
            with open("app/streamlit_ui/default_answer_sheet.pdf", "rb") as f:
                uploaded_file = BytesIO(f.read())
                uploaded_file.name = "default_answer_sheet.pdf"
        except FileNotFoundError:
            st.error("Please upload a PDF file or ensure default_answer_sheet.pdf exists.")
            st.stop()

    # Make the POST request
    with st.spinner("Marking in progress..."):
        response = requests.post(
            api_url,
            data={"data": json.dumps(parsed_data)},
            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        )

    # Handle response
    if response.status_code == 200:
        st.success("Sheet marked successfully!")
        response_data = response.json()
        st.session_state["marked_sheet"] = response_data

        st.subheader("📊 Marks Breakdown")
        for q in response_data["list_of_questions"]:
            st.markdown(f"### Question {q['question_number']}")
            st.markdown(f"**Total Marks Awarded**: {q['total_marks']}")
            st.markdown(f"**Presentation Score**: {q['presentation_score']}")
            st.markdown("**Rubric Marks**:")
            for marks, rubric in q["rubrics_marks"]:
                st.markdown(f"- {rubric}: {marks}")
            if q.get("feedback"):
                st.markdown(f"**Feedback**: {q['feedback']}")
    else:
        st.error(f"API Error [{response.status_code}]: {response.text}")
        
# Download PDF button
if "marked_sheet" in st.session_state:
    response_data = st.session_state["marked_sheet"]
    pdf_bytes = generate_pdf(response_data)
    st.download_button(
        label="Download Marked Sheet PDF",
        data=pdf_bytes,
        file_name="marked_subjective_sheet.pdf",
        mime="application/pdf"
    )
