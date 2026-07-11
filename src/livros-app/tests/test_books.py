import pytest

from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')

    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()

    response = client.get('/')

    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'test author' in response.data
    assert b'test\nreview' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    'path',
    (
        '/create',
        '/1/update',
        '/1/delete',
    )
)
def test_login_required(client, path):
    response = client.post(path)

    assert response.headers['Location'] == '/auth/login'


def test_owner_required(app, client, auth):
    # Altera o dono do livro para outro usuário.
    with app.app_context():
        db = get_db()

        db.execute(
            'UPDATE book SET owner_id = 2 WHERE id = 1'
        )

        db.commit()

    auth.login()

    # O usuário atual não pode alterar o livro de outro usuário.
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403

    # O usuário atual não deve visualizar o link de edição.
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize(
    'path',
    (
        '/2/update',
        '/2/delete',
    )
)
def test_exists_required(client, auth, path):
    auth.login()

    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()

    assert client.get('/create').status_code == 200

    client.post(
        '/create',
        data={
            'title': 'created',
            'book_author': 'created author',
            'review': '',
        }
    )

    with app.app_context():
        db = get_db()

        count = db.execute(
            'SELECT COUNT(id) FROM book'
        ).fetchone()[0]

        assert count == 2


def test_update(client, auth, app):
    auth.login()

    assert client.get('/1/update').status_code == 200

    client.post(
        '/1/update',
        data={
            'title': 'updated',
            'book_author': 'updated author',
            'review': 'updated review',
        }
    )

    with app.app_context():
        db = get_db()

        book = db.execute(
            'SELECT * FROM book WHERE id = 1'
        ).fetchone()

        assert book['title'] == 'updated'
        assert book['book_author'] == 'updated author'
        assert book['review'] == 'updated review'


@pytest.mark.parametrize(
    'path',
    (
        '/create',
        '/1/update',
    )
)
def test_create_update_validate(client, auth, path):
    auth.login()

    response = client.post(
        path,
        data={
            'title': '',
            'book_author': 'author',
            'review': 'review',
        }
    )

    assert b'Title is required.' in response.data


def test_create_validate_author(client, auth):
    auth.login()

    response = client.post(
        '/create',
        data={
            'title': 'title',
            'book_author': '',
            'review': 'review',
        }
    )

    assert b'Author is required.' in response.data


def test_create_validate_review(client, auth):
    auth.login()

    response = client.post(
        '/create',
        data={
            'title': 'title',
            'book_author': 'author',
            'review': '',
        }
    )

    assert b'Review is required.' in response.data


def test_delete(client, auth, app):
    auth.login()

    response = client.post('/1/delete')

    assert response.headers['Location'] == '/'

    with app.app_context():
        db = get_db()

        book = db.execute(
            'SELECT * FROM book WHERE id = 1'
        ).fetchone()

        assert book is None