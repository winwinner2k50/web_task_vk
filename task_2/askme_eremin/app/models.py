from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading_question = models.CharField(max_length=255)
    question_text = models.TextField()
    # answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, null=True, blank=True)
    likes_user = models.ManyToManyField(User, through='QuestionLike', related_name='liked_questions', blank=True) 

    def __str__(self):
        return self.heading_question

    def likes_count(self):
        return self.likes_user.count()



class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    answer_text = models.TextField()
    right = models.BooleanField()
    likes_user = models.ManyToManyField(User, through='AnswerLike', related_name='liked_answers', blank=True)

    def __str__(self):
        return self.answer_text[:50]

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['question', 'tag']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'question'] 

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'answer'] 