import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def handle(self, *args, **kwargs):
        # Количество объектов
        num_users = 10000
        num_questions = 100000
        num_answers = 1000000
        num_tags = 10000
        num_likes = 2000000
        count_likes = 0

        self.stdout.write("Создаём пользователей...")
        user_instances = [
            User(username=f'user_{i}', email=f'user_{i}@example.com', password='password')
            for i in range(num_users)
        ]
        User.objects.bulk_create(user_instances)
        users = list(User.objects.all())

        self.stdout.write("Создаём профили...")
        profile_instances = [
            Profile(user=user) for user in users
        ]
        Profile.objects.bulk_create(profile_instances)

        self.stdout.write("Создаём теги...")
        tag_instances = [
            Tag(tag_name=f'tag_{i}') for i in range(num_tags)
        ]
        Tag.objects.bulk_create(tag_instances)
        tags = list(Tag.objects.all())

        self.stdout.write("Создаём вопросы...")
        question_instances = [
            Question(
                heading_question=f'Question {i}',
                question_text=f'Text of question {i}',
                user=random.choice(users)
            )
            for i in range(num_questions)
        ]
        Question.objects.bulk_create(question_instances)
        questions = list(Question.objects.all())

        self.stdout.write("Создаём ответы...")
        answer_instances = [
            Answer(
                answer_text=f'Answer {i}',
                right=random.choice([True, False]),
                user=random.choice(users)
            )
            for i in range(num_answers)
        ]
        Answer.objects.bulk_create(answer_instances)
        answers = list(Answer.objects.all())

        self.stdout.write("Связываем вопросы с ответами...")
        for question in questions:
            question.answer = random.choice(answers)
        Question.objects.bulk_update(questions, ['answer'])

        self.stdout.write("Добавляем лайки к вопросам...")
        for question in questions:
            if (count_likes % 1000 == 0):
                print(count_likes)
            if (count_likes > num_likes/4):
                break
            chosen_users = random.sample(users, 4)
            for user in chosen_users:
                if not QuestionLike.objects.filter(user=user, question=question).exists():
                    QuestionLike.objects.create(user=user, question=question)
                    count_likes += 1


        self.stdout.write("Добавляем лайки к ответам...")
        for answer in answers:
            if (count_likes % 1000 == 0):
                print(count_likes)
            if (count_likes > num_likes):
                break
            chosen_users = random.sample(users, 4)
            for user in chosen_users:
                if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                    AnswerLike.objects.create(user=user, answer=answer)
                    count_likes+=1

        self.stdout.write("Связываем теги с вопросами...")
        question_tag_instances = [
            (question, random.sample(tags, k=5)) for question in questions
        ]
        for question, tag_set in question_tag_instances:
            question.tags.add(*tag_set)

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
