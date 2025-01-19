"""
URL configuration for askme_eremin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from app.views import login_view
from app.views import question_detail

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("settings/", views.settings, name="settings"),
    path('login/', login_view, name='login'),
    path("signup/", views.signup, name="signup"),
    path("tag/", views.tag, name="tag"),
    path("ask/", views.ask, name="ask"),
    path('question/<int:question_id>/', views.question_detail, name='question'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
