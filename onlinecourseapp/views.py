from django.shortcuts import get_object_or_404, render, redirect

from .models import Course, Question, Choice


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "course_details_bootstrap.html",
        {"course": course}
    )
def exam(request):
    questions = Question.objects.all()

    return render(
        request,
        "exam.html",
        {"questions": questions}
    )

def submit(request):
    if request.method == "POST":
        score = 0
        total_questions = Question.objects.count()

        for question in Question.objects.all():
            selected_choice_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(
                        id=selected_choice_id,
                        question=question
                    )

                    if selected_choice.is_correct:
                        score += 1

                except Choice.DoesNotExist:
                    pass

        request.session["score"] = score
        request.session["total_questions"] = total_questions

        return redirect("show_exam_result")

    return redirect("course_details", course_id=1)


def show_exam_result(request):
    score = request.session.get("score", 0)
    total_questions = request.session.get("total_questions", 0)

    return render(
        request,
        "exam_result.html",
        {
            "score": score,
            "total_questions": total_questions,
        }
    )