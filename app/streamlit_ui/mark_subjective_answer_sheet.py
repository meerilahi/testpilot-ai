import streamlit as st
import requests
import json

st.title("📄 Subjective Sheet Auto-Marking (BISEP Style)")

# Input FastAPI URL
api_url = st.text_input("FastAPI Endpoint URL", "http://localhost:8000/mark_bisep_subjective")

# Upload PDF file
uploaded_file = st.file_uploader("Upload Answer Sheet (PDF)", type=["pdf"])

# JSON input field for MarkSubjectiveSheetRequest
st.subheader("📝 Enter Marking Instructions (JSON Format)")
default_json = {
    "list_of_questions": [
        {
            "question_number": 1,
            "pages": [1],
            "q_type": "RRQ",
            "question_text": "Define photosynthesis.",
            "answer_key": "Photosynthesis is the process...",
            "diagram_key": None,
            "rubrics": [
                [1, "Definition"],
                [1, "Process explained"],
                [1, "Scientific terms used"]
            ],
            "grammer_penalty": "Low",
            "question_marks": 3.0
        }
    ],
    "rrq_questions": 1,
    "erq_questions": 0,
    "total_paper_marks": 3.0,
    "language": "English",
    "subject": "Biology"
}

input_data = st.text_area("Request JSON", value=json.dumps(default_json, indent=2), height=300)

# Submit Button
if st.button("Mark Answer Sheet"):
    if uploaded_file is None or not input_data:
        st.error("Please upload a PDF file and provide JSON data.")
    else:
        try:
            parsed_data = json.loads(input_data)
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
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
            st.json(response_data)

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
