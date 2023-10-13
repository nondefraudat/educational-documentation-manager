from .db import get_db 
from flask import Blueprint, flash, g, redirect,\
        render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/firsttime', methods=('GET', 'POST'))
def firsttime():
    db = get_db()
    if int(db.execute('SELECT count(*) FROM User').fetchone()[0]) != 0:
        return redirect(url_for('index'))
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password_repeat = request.form['password-repeat']
        error = None
        if not password:
            error = 'Пароль не введен!'
        elif password != password_repeat:
            error = 'Пароли не совпадают!'
        if not error:
            try:
                db.execute('INSERT INTO User (Login, PasswordHash, Rights) VALUES (?, ?, ?)',
                        (login, generate_password_hash(password), 'root'))
                db.commit()
            except db.IntegrityError:
                error = f'Ошибка при выполнении операции'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/firsttime.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()
    if int(db.execute('SELECT count(*) FROM User').fetchone()[0]) == 0:
        return redirect(url_for('auth.firsttime'))
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        error = None
        user = db.execute('SELECT * FROM User WHERE Login = ?', (login,)).fetchone()
        if not user:
            error = 'Такого логина не существует!'
        elif not check_password_hash(user['PasswordHash'], password):
            error = 'Пароль неверный!'
        if not error:
            session.clear()
            session['user_id'] = user['Id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM User WHERE Id = ?',
                (user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
