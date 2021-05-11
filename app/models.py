from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, verbose_name='User name')
    profile_pic = ResizedImageField(size=[60, 60], upload_to='avatars', verbose_name='Аватар')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True, verbose_name='Tag`s name')

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-creation_date")

    def hot_questions(self):
        return self.order_by("-rating")

    def questions_for_tag(self, tag):
        return self.filter(tags__tag_name=tag)


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Question title')
    content = models.TextField(verbose_name='Question text')
    rating = models.IntegerField(default=0, verbose_name='Question rating')
    creation_date = models.DateTimeField(verbose_name='Question creation date')
    tags = models.ManyToManyField('Tag', verbose_name='ags', related_name='questions', related_query_name='question')
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Question ratings", through='QuestionVote',
                                   related_name="voted_questions", related_query_name="voted_questions")

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def update_rating(self):
        self.rating = QuestionVote.objects.get_rating(self.id)
        self.save()

    def get_answers_count(self):
        return self.answers.count()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class AnswerManager(models.Manager):
    def best_answers(self):
        return self.order_by("-rating")


class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers",
                                         related_query_name="answer")
    content = models.TextField(verbose_name='Response text')
    rating = models.IntegerField(default=0, verbose_name='Response rating')
    creation_date = models.DateTimeField(verbose_name='Response creation date')
    is_marked_correct = models.BooleanField(default=False, verbose_name='Is it marked as correct')
    votes = models.ManyToManyField('Profile', blank=True, verbose_name="Question ratings", through='AnswerVote',
                                   related_name="voted_answer", related_query_name="voted_answer")
    objects = AnswerManager()

    def __str__(self):
        return self.content

    def update_rating(self):
        self.rating = AnswerVote.objects.get_rating(self.id)
        self.save()

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class VoteManager(models.Manager):
    LIKE = 1
    DISLIKE = -1

    def get_likes(self, pk):
        return self.filter(id=pk, mark=VoteManager.LIKE).count()

    def get_dislikes(self, pk):
        return self.filter(id=pk, mark=VoteManager.DISLIKE).count()

    def get_rating(self, pk):
        return self.get_likes(pk) - self.get_dislikes(pk)


class QuestionVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Who rated it')
    mark = models.IntegerField(default=0,
                               verbose_name='Assigned rating')

    objects = VoteManager()

    related_question = models.ForeignKey('Question', verbose_name='Evaluated question', on_delete=models.CASCADE)

    def __str__(self):
        return f'Question assessment: {self.mark}'

    class Meta:
        verbose_name = 'Question assessment'
        verbose_name_plural = 'Questions assessment'


class AnswerVote(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Who rated it')
    mark = models.IntegerField(default=0,
                               verbose_name='Assigned rating')

    objects = VoteManager()

    related_answer = models.ForeignKey('Answer', verbose_name='Rated response', on_delete=models.CASCADE)

    def __str__(self):
        return f'Response rating: {self.mark}'

    class Meta:
        verbose_name = 'Response of answer'
        verbose_name_plural = 'Responses of answers'


class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class ArticleManager(models.Manager):
    def only_from_marina(self):
        return self.filter(author_id=1)




