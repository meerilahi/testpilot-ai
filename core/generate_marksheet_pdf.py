from fpdf import FPDF
from schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetResponse


def generate_marksheet_pdf(response: MarkSubjectiveAnswerSheetResponse, output_path="marked_response.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Student ID: {response.student_id}", ln=True, align="L")
    pdf.ln(5)

    for q in response.list_of_evaluated_answers:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Question {q.question_number}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 8, txt=f"Attempted: {'Yes' if q.isAttempted else 'No'}", ln=True)

        if q.rubrics_marks:
            pdf.cell(200, 8, txt="Rubrics:", ln=True)
            for rubric, mark in q.rubrics_marks:
                # Changed bullet to hyphen to avoid Unicode error
                pdf.multi_cell(0, 8, txt=f"  - {rubric} : {mark} marks")

        if q.presentation_score is not None:
            pdf.cell(200, 8, txt=f"Presentation Score: {q.presentation_score}", ln=True)

        if q.feedback:
            pdf.multi_cell(0, 8, txt=f"Feedback: {q.feedback}")

        if q.total_marks is not None:
            pdf.cell(200, 8, txt=f"Total Marks: {q.total_marks}", ln=True)

        pdf.ln(5)

    pdf.output(output_path)
    print(f"✅ PDF saved to: {output_path}")