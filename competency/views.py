from django.shortcuts import render, redirect
from .utils import generate_questions_for_job, save_generated_questions
from .models import Question
from .utils import evaluate_answer
from django.db.models import Avg

def generate_test_questions(request):
    if request.method == 'POST':
        job_role = request.POST.get('job_role')
        if job_role:
            raw_output = generate_questions_for_job(job_role)
            save_generated_questions(raw_output, job_role)
            return redirect('view_questions', job_role=job_role)
    return render(request, 'competency/generate_test.html')

def view_questions(request, job_role):
    questions = Question.objects.filter(job_role=job_role)
    return render(request, 'competency/view_questions.html', {'questions': questions, 'job_role': job_role})


from .models import CompetencyTestSession, Question, Answer
from django.contrib.auth.decorators import login_required

@login_required
def start_test(request, job_role):
    session = CompetencyTestSession.objects.create(user=request.user, job_role=job_role)

    # Get first question for job
    question = Question.objects.filter(job_role=job_role).order_by('?').first()
    return redirect('question', session_id=session.id, question_id=question.id)

@login_required
def question_view(request, session_id, question_id):
    session = CompetencyTestSession.objects.get(id=session_id, user=request.user)
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        answer= request.POST.get('answer')
        my_answer = Answer.objects.create(
            session=session,
            question=question,
            selected_answer=answer,
            is_correct=False  # Optional: Add answer checking later
        )
        

        # After saving the answer
        score = evaluate_answer(question.text, answer)
        Answer.objects.filter(id=my_answer.id).update(
            is_correct=score >= 0.5  # Binary correctness
        )


        # Fetch next unanswered question
        answered_ids = Answer.objects.filter(session=session).values_list('question_id', flat=True)
        next_question = Question.objects.filter(job_role=session.job_role).exclude(id__in=answered_ids).order_by('?').first()

        if next_question:
            return redirect('question', session_id=session.id, question_id=next_question.id)
        else:
            session.completed = True
            session.score = 0  # Optional: add real scoring
            session.save()
            return redirect('test_result', session_id=session.id)
        
        

    return render(request, 'competency/test_question.html', {
        'session': session,
        'question': question
    })

@login_required
def test_result(request, session_id):
    session = CompetencyTestSession.objects.get(id=session_id, user=request.user)
    answers = Answer.objects.filter(session=session)
    
    score = Answer.objects.filter(session=session).aggregate(avg_score=Avg('is_correct'))['avg_score'] or 0
    session.score = round(score * 100, 2)  # Convert to %
    session.completed = True
    session.save()
    return render(request, 'competency/test_result.html', {
        'session': session,
        'answers': answers
    }) 
    
@login_required
def history_test(request):
    sessions = CompetencyTestSession.objects.filter(user=request.user)
    return render(request, 'competency/history_test.html', {'sessions': sessions})



# @login_required
# def history_graph(request):
#     sessions = CompetencyTestSession.objects.filter(user=request.user).order_by('created_at')

#     # Preprocess performance data
#     for session in sessions:
#         answers = session.answer_set.all()
#         total = answers.count()
#         correct = answers.filter(is_correct=True).count()
#         percentage = round((correct / total) * 100) if total > 0 else 0

#         # Attach data to each session
#         session.total = total
#         session.correct = correct
#         session.percentage = percentage

#     return render(request, 'competency/graphs.html', {'sessions': sessions})
from django.db.models import Count, Case, When, IntegerField, FloatField
from django.db.models.functions import Cast


@login_required
def history_graph(request):
    sessions = CompetencyTestSession.objects.filter(user=request.user).annotate(
        total_questions=Count('answer'),
        correct_answers=Count(Case(When(answer__is_correct=True, then=1))),
        accuracy=Cast('correct_answers', FloatField()) / Cast('total_questions', FloatField()) * 100
    ).order_by('created_at')
    
    # Calculate totals
    total_correct = sum(session.correct_answers for session in sessions)
    total_questions = sum(session.total_questions for session in sessions)
    overall_accuracy = round((total_correct / total_questions) * 100, 1) if total_questions > 0 else 0
    
    return render(request, 'competency/graphs.html', {
        'sessions': sessions,
        'total_correct': total_correct,
        'overall_accuracy': overall_accuracy
    })