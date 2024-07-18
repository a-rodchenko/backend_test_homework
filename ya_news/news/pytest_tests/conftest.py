import pytest
from datetime import datetime, timedelta


from django.test.client import Client
from django.conf import settings
from django.utils import timezone


from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Эстонцы в Осло',
        text='Эстонцы сегодня приземлились в Осло',
    )
    return news


@pytest.fixture
def first_comment_text():
    return 'Добро пожаловать, эстонцы!'


@pytest.fixture
def comment(news, author, first_comment_text):
    comment = Comment.objects.create(news=news,
                                     author=author,
                                     text=first_comment_text, )
    return comment


@pytest.fixture
def many_news():
    many_news = [
        News(title=f'Новость {index}', text='Просто текст.',
             date=datetime.today() - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)]
    News.objects.bulk_create(many_news)
    return


@pytest.fixture
def home_url():
    return 'news:home'


@pytest.fixture
def news_with_comments(news, author):
    for index in range(10):
        comment = Comment.objects.create(news=news,
                                         author=author,
                                         text=f'Эстонцы, их уже: {index}', )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
    return news


@pytest.fixture
def comment_text():
    return 'Эстонцы, кругом одни эстонцы'


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}
