from .db import get_db 
from flask import Blueprint, flash, g, redirect,\
        render_template, request, session, url_for
from .auth import login_required

bp = Blueprint('admforms', __name__, url_prefix='/admforms')

@bp.route('/teachers', methods=('GET', 'POST'))
@login_required
def teachers():
    db = get_db()
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        department_name = request.form['department']
        faculty_name = request.form['faculty']
        rank_name = request.form['rank']
        position_name = request.form['position']
        degree_name = request.form['degree']

        error = None
        if not surname:
            error = 'Не указана фамилия!'
        elif not name:
            error = 'Не указано имя!'
        elif not patronymic:
            error = 'Не указано отчество!'
        elif not department_name:
            error = 'Не указана кафедра!'
        elif not faculty_name:
            error = 'Не указан факультет!'
        elif not rank_name:
            error = 'Не указано звание!'
        elif not position_name:
            error = 'Не указана должность!'
        elif not degree_name:
            error = 'Не указана ученая степень!'

        if not error:
            try:
                department_id = None
                department = db.execute('SELECT * FROM Department WHERE "Name" = ?',
                        (department_name,)).fetchone()
                if department:
                    department_id = department.get('Id')
                else:
                    department_id = db.execute('INSERT INTO Department ("Name") VALUES (?)',
                            (department_name,)).lastrowid
                    db.commit()
                
                faculty_id = None
                faculty = db.execute('SELECT * FROM Faculty WHERE "Name" = ?',
                        (faculty_name,)).fetchone()
                if faculty:
                    faculty_id = faculty.get('Id')
                else:
                    faculty_id = db.execute('INSERT INTO Faculty ("Name") VALUES (?)',
                            (faculty_name,)).lastrowid
                    db.commit()

                rank_id = None
                rank = db.execute('SELECT * FROM Rank WHERE "Name" = ?',
                        (rank_name,)).fetchone()
                if rank:
                    rank_id = rank.get('Id')
                else:
                    rank_id = db.execute('INSERT INTO Rank ("Name") VALUES (?)',
                            (rank_name,)).lastrowid
                    db.commit()

                position_id = None
                position = db.execute('SELECT * FROM Position WHERE "Name" = ?',
                        (position_name,)).fetchone()
                if position:
                    position_id = position.get('Id')
                else:
                    position_id = db.execute('INSERT INTO Position ("Name") VALUES (?)',
                            (position_name,)).lastrowid
                    db.commit()

                degree_id = None
                degree = db.execute('SELECT * FROM Degree WHERE "Name" = ?',
                        (degree_name,)).fetchone()
                if degree:
                    degree_id = degree.get('Id')
                else:
                    degree_id = db.execute('INSERT INTO Degree ("Name") VALUES (?)',
                            (degree_name,)).lastrowid
                    db.commit()
                
                db.execute('INSERT INTO Teacher ("Name", Surname, Patronymic, DepartmentId, FacultyId, RankId, PositionId, DegreeId) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (name, surname, patronymic, department_id, faculty_id, rank_id, position_id, degree_id))
                db.commit()

            except db.IntegrityError:
                error = f'Ошибка при выполнении операции'
            else:
                return redirect(url_for('admforms.teachers'))
        flash(error)
    return render_template('admforms/teachers.html', teachers=db.execute('SELECT * FROM Teacher').fetchall())

