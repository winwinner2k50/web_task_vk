from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    questions_page = paginate(QUESTIONS, request, per_page)
    return render(request, template_name="index.html", context={'questions': questions_page})

def hot(request):
    return render(request, template_name="hot.html", context={'questions' : QUESTIONS })

def tag(request, tag_id):
    return render(request, template_name="tag.html", context={'questions' : QUESTIONS })

def question(request, id):
    return render(request, template_name="question.html", context={'questions' : QUESTIONS })

def settings(request):
    return render(request, template_name="settings.html", context={'questions' : QUESTIONS })

def signup(request):
    return render(request, template_name="signup.html", context={'questions' : QUESTIONS })

def login(request):
    return render(request, template_name="login.html", context={'questions' : QUESTIONS })


def ask(request):
    return render(request, template_name="ask.html", context={'questions' : QUESTIONS })
