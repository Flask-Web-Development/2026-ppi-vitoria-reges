from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('books', __name__)

@bp.route('/')
def index():
    db = get_db()

    books = db.execute(
        'SELECT b.id, title, book_author, review, created, owner_id, username'
        ' FROM book b JOIN user u ON b.owner_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('books/index.html', books=books)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        book_author = request.form['book_author']
        review = request.form['review']
        error = None

        if not title:
            error = 'Title is required.'
        elif not book_author:
            error = 'Author is required.'
        elif not review:
            error = 'Review is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (title, book_author, review, owner_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, book_author, review, g.user['id'])
            )
            db.commit()
            return redirect(url_for('books.index'))

    return render_template('books/create.html')

def get_book(id, check_author=True):
    book = get_db().execute(
        'SELECT b.id, title, book_author, review, created, owner_id, username'
        ' FROM book b JOIN user u ON b.owner_id = u.id'
        ' WHERE b.id = ?',
        (id,)
    ).fetchone()

    if book is None:
        abort(404, f"Book id {id} doesn't exist.")

    if check_author and book['owner_id'] != g.user['id']:
        abort(403)

    return book

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    book = get_book(id)

    if request.method == 'POST':
        title = request.form['title']
        book_author = request.form['book_author']
        review = request.form['review']
        error = None

        if not title:
            error = 'Title is required.'
        elif not book_author:
            error = 'Author is required.'
        elif not review:
            error = 'Review is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE book'
                ' SET title = ?, book_author = ?, review = ?'
                ' WHERE id = ?',
                (title, book_author, review, id)
            )
            db.commit()
            return redirect(url_for('books.index'))

    return render_template('books/update.html', book=book)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_book(id)
    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('books.index'))