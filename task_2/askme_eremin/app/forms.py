from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
from .models import Question, Answer
from django.shortcuts import redirect

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")
    avatar = forms.ImageField(required=False, label="Аватар")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password', 'confirm_password', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        if not user.pk:
            user.save()

        profile, created = Profile.objects.get_or_create(user=user)

        if 'avatar' in self.cleaned_data:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

        if commit:
            user.save()

        return user

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Неверный логин или пароль.")
            if not user.is_active:
                raise forms.ValidationError("Аккаунт отключен.")
        return cleaned_data


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

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'right']


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, label="Теги", help_text="Введите теги через запятую")

    class Meta:
        model = Question
        fields = ['heading_question', 'question_text', 'tags']

    def clean_tags(self):
        tags_data = self.cleaned_data.get('tags')
        if tags_data:
            tags = [tag.strip() for tag in tags_data.split(',')]
            return tags
        return []