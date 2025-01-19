from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from .forms import CustomLoginForm
from .forms import AnswerForm
from .forms import QuestionForm
from .models import Tag, QuestionTag
from django.db.models import Count

QUESTIONS = [
    {
        'title': 'title' + str(i),
        'id': i,
        'text': 'text' + str(i)
    } for i in range(1,15)
]

def paginate(objects_list, request, per_page):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    paginator = Paginator(objects_list, per_page)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
    

def index(request):
    per_page = 3
    questions_list = Question.objects.prefetch_related('answers', 'questiontag_set__tag')
    questions_page = paginate(questions_list, request, per_page)
    return render(request, template_name="index.html", context={'questions': questions_page})

def hot(request):
    per_page = 3
    questions_list = Question.objects.annotate(likes_count=Count('likes_user')).order_by('-likes_count')
    questions_page = paginate(questions_list, request, per_page)
    return render(request, template_name="hot.html", context={'questions': questions_page})

def tag(request):
    tag_name = request.GET.get('name')
    if not tag_name:
        return render(request, "tag.html", {"questions": [], "tag_name": "Неизвестный тег"})

    tag = get_object_or_404(Tag, tag_name=tag_name)
    question_tags = QuestionTag.objects.filter(tag=tag)
    questions = [qt.question for qt in question_tags]

    return render(request, "tag.html", {"questions": questions, "tag_name": tag.tag_name})


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question

            if request.user.is_authenticated:
                answer.user = request.user
            else:
                pass

            answer.save()

            print("ok")
            return redirect('question', question_id=question.id)
        else:
            print(form.errors)
    else:
        form = AnswerForm()

    return render(request, 'question.html', {'question': question, 'answers': answers, 'form': form})

def settings(request):
    return render(request, template_name="settings.html", context={'questions' : QUESTIONS })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Ошибка аутентификации')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            question = form.save(commit=False)
            question.user = request.user
            question.save()


            if 'tags' in request.POST:
                tags = request.POST['tags'].split(',')
                errors = []

                for tag_name in tags:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                        QuestionTag.objects.create(question=question, tag=tag)
                    else:
                        errors.append('Некорректное имя тега.')

                if errors:
                    return render(request, 'ask.html', {'form': form, 'errors': errors})

            return redirect('index')

    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})

def add_answer(request, question_id):
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        if answer_text:
            question = Question.objects.get(pk=question_id)
            Answer.objects.create(
                user=request.user,
                answer_text=answer_text,
                right=False,
                question=question
            )
        return redirect('question', id=question_id)