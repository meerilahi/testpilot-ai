from schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetResponse, QuestionResponse,MarkSubjectiveAnswerSheetRequest
def prepare_response(mark_sheet, student_id, presentation_scores, request:MarkSubjectiveAnswerSheetRequest, attempted_qns_mask) -> MarkSubjectiveAnswerSheetResponse:
    evaluated_answers = []

    for question in request.list_of_questions:
        
        qn = question.question_number
        if not attempted_qns_mask[qn]:
            evaluated_answers.append(
                QuestionResponse(
                    question_number=qn,
                    isAttempted=False,
                    rubrics_marks=None,
                    presentation_score=None,
                    feedback=None,
                    total_marks=None
                )
            )
            continue

        evaluated_answers.append(
            QuestionResponse(
                question_number=qn,
                isAttempted=True,
                rubrics_marks=mark_sheet.get(qn, {}).get("rubrics", []),
                presentation_score=presentation_scores.get(qn, None),
                feedback=mark_sheet.get(qn, {}).get("feedback", None),
                total_marks=mark_sheet.get(qn, {}).get("marks", None)
            )
        )

    return MarkSubjectiveAnswerSheetResponse(
        student_id=student_id,
        list_of_evaluated_answers=evaluated_answers,
    )


