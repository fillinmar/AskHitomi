from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware

from app.models import *

from random import choice, sample, randint
from faker import Faker
from datetime import datetime

fake = Faker(["ru_RU"])


def generate_users():
    for i in range(100):
        User.objects.create_user(fake.unique.first_name()+"Ii1", fake.email(),
                                 fake.password(length=fake.random_int(min=8, max=15)))


class Command(BaseCommand):
    help = 'Generate database'

    def add_arguments(self, parser):
        parser.add_argument("--profiles", type=int, help="Numbers of profile")
        parser.add_argument("--questions", type=int, help="Numbers of questions")
        parser.add_argument("--answers", type=int, help="Numbers of question`s answers")
        parser.add_argument("--tags", type=int, help="Numbers of tags")
        parser.add_argument("--votes", type=int, help="Numbers of questions`s votes")

    def handle(self, *args, **kwargs):
        try:
            profiles_count = kwargs["profiles"]
            questions_count = kwargs["questions"]
            answers_per_question_count = kwargs["answers"]
            tags_count = kwargs["tags"]
        except:
            raise CommandError("Some arguments were not provided")

        self.generate_profiles(profiles_count)
        self.generate_tags(tags_count)
        self.generate_questions(questions_count)
        self.generate_answers(answers_per_question_count)

    def generate_profiles(self):
        generate_users(100)
        users_ids = list(User.objects.values_list("id", flat=True))
        profile_pics = ["img/profile-pic.jpeg", "img/hitomi3.jpeg"]

        for i in range(100):
            Profile.objects.create(user_id=users_ids[i], user_name=fake.last_name()+i,
                                   profile_pic=choice(profile_pics))

    def generate_tags(self):
        for i in range(100):
            Tag.objects.create(tag_name=fake.word())

    def generate_questions(self, count):
        profiles = list(Profile.objects.values_list("id", flat=True))
        for i in range(100):
            question = Question.objects.create(
                author_id=choice(profiles),
                title=fake.sentence(nb_words=3),
                content=fake.text(),
                creation_date=fake.date_time_between(make_aware(datetime(year=2019, month=1, day=1),
                                                                timezone.get_current_timezone()),
                                                     timezone.now())
            )
            tags_count = Tag.objects.count()
            tags = list(set([Tag.objects.get(id=randint(1, tags_count)) for _ in range(randint(1, tags_count))]))
            question.tags.set(tags)

            question.votes.set(sample(profiles, randint(1, len(profiles))),
                               through_defaults={"mark": VoteManager.LIKE})
            question.update_rating()

    def generate_answers(self):
        profiles = list(Profile.objects.values_list("id", flat=True))
        questions = list(Question.objects.values_list("id", flat=True))
        for question_id in questions:
            for i in range(100):
                answer = Answer.objects.create(
                    author_id=choice(profiles),
                    related_question_id=question_id,
                    content=fake.text(),
                    creation_date=fake.date_time_between(make_aware(datetime(year=2020, month=10, day=1),
                                                                    timezone.get_current_timezone()),
                                                         timezone.now())
                )
