import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urls',
    ('news:home', 'users:login', 'users:logout', 'users:signup', )
)
def test_pages_availability_for_anonymous_user(client, urls):
    url = reverse(urls)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page(client, news):
    url = reverse('news:detail', args=(news.pk, ))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_data',
    (('news:edit', HTTPStatus.OK, 'author_client', ),
     ('news:edit', HTTPStatus.NOT_FOUND, 'not_author_client', ),
     ('news:delete', HTTPStatus.OK, 'author_client', ),
     ('news:delete', HTTPStatus.NOT_FOUND, 'not_author_client', ), ))
def test_availability_comment_edit_and_delete(test_data, comment,
                                              request: pytest.FixtureRequest):
    url, expected, user = test_data
    client = request.getfixturevalue(user)
    urls = reverse(url, args=(comment.id, ))
    response = client.get(urls)
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urls',
    ('news:edit', 'news:delete', ))
def test_redirect_for_anonymous_client(urls, client, comment):
    login_url = reverse('users:login')
    url = reverse(urls, args=(comment.id, ))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
