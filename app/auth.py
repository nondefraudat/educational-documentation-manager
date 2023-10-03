from .db import get_db 
from flask import Blueprint, flash, g, redirect,\
        render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        db = get_db()
        error = None

        if not login:
            error = 'Введите логин'
        elif not password:
            error = 'Введите пароль'

        if error is None:
            try:
                db.execute('INSERT INTO User (Login, PasswordHash, Rights) VALUES (?, ?, ?)',
                        (login, generate_password_hash(password), 'test'))
                db.commit()
            except db.IntegrityError:
                error = f'Пользователь с таким логином уже существует'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
        
    return render_template('auth/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM User WHERE Login = ?', (login,)).fetchone()
        if not user:
            error = 'Неверный логин'
        elif not check_password_hash(user['PasswordHash'], password):
            error = 'Неверный пароль'

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
