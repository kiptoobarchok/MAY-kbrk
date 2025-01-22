from flask import Blueprint
from application import db
from flask import render_template, url_for, redirect,  request, abort
from application.lessons.forms import (AddLessonForm, AddBodyForm)
from application.models import Lesson, Body
from flask_login import current_user,  login_required


lessons_bp = Blueprint('lessons', __name__)

## Lessons
@lessons_bp.route('/lessons', methods=['GET'])
@login_required
def lessons():
    page = request.args.get('page', 1, type=int)
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(page=page, per_page=10)
    print(type(lessons))  # Check the type of `lessons`
    return render_template('lessons.html', title='Sabbath Lessons', lessons=lessons)


@lessons_bp.route('/add_lesson', methods=['GET', 'POST'])
@login_required
def add_lesson():
    if current_user.role != 'admin':
      abort(403)
    form = AddLessonForm()
    if form.validate_on_submit():
        lesson = Lesson(title=form.title.data,date_posted=form.date_posted.data, scripture_reading=form.scripture_reading.data, memory_verse=form.memory_verse.data, introduction=form.introduction.data, conclusion=form.conclusion.data)
        db.session.add(lesson)
        db.session.commit()
        print('lesson added...')
        return redirect(url_for('lessons.lessons'))
    print('failed to add')
    return render_template('add_lesson.html', title='Add Lesson' , form=form)

@lessons_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
@login_required  
def view_lesson(lesson_id):
    # Fetch the lesson from the database by its ID
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('view_lesson.html', title=lesson.title, lesson=lesson)

## update lesson

@lessons_bp.route('/lesson/<int:lesson_id>/update', methods=['GET', 'POST'])
@login_required  
def update_lesson(lesson_id):
    if current_user.role != 'admin':
      abort(403)
    # Fetch the lesson from the database by its ID
    lesson = Lesson.query.get_or_404(lesson_id)
    form = AddLessonForm()
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.date_posted = form.date_posted.data
        lesson.scripture_reading = form.scripture_reading.data
        lesson.memory_verse = form.memory_verse.data
        lesson.introduction = form.introduction.data
        lesson.conclusion = form.conclusion.data
        db.session.commit()
        db.session.refresh(lesson)
        print('update successful')
        return redirect(url_for('lessons.lessons', lesson_id=lesson.id))
    elif request.method == 'GET':
        form.title.data = lesson.title
        form.date_posted.data = lesson.date_posted 
        form.scripture_reading.data = lesson.scripture_reading
        form.memory_verse.data = lesson.memory_verse
        form.introduction.data = lesson.introduction
        form.conclusion.data = lesson.conclusion
    return render_template('update_lesson.html', title=lesson.title, lesson=lesson, form=form)

@lessons_bp.route('/add_content', methods=['GET', 'POST'])
@login_required  
def add_content():
    if current_user.role != 'admin':
      abort(403)
    form =AddBodyForm()
    if form.validate_on_submit():
        body = Body(question=form.question.data, answers=form.answers.data, lesson_id=form.lesson_id.data)
        db.session.add(body)
        db.session.commit()
        return redirect(url_for('lessons.lessons'))
    print('unsuccessful')
    return render_template('add_content.html', title='Add Q and A', form=form)

@lessons_bp.route('/lesson/<int:lesson_id>/body', methods=['GET'])
@login_required  
def view_body(lesson_id):
    body = Body.query.filter_by(lesson_id=lesson_id).all()
    return render_template('view_body.html', title='Question and Answers' , body=body)


## update question and answers
@lessons_bp.route('/lesson/<int:lesson_id>/body/<int:body_id>', methods=['GET', 'POST'])
@login_required  
def update_body(lesson_id, body_id):
    body = Body.query.filter_by(lesson_id).first(body_id)
    form = AddBodyForm()
    if form.validate_on_submit():
        body.question = form.question.data
        body.answers = form.answers.data
        body.lesson_id = form.lesson_id.data
        db.session.commit()
        db.session.refresh(body)
        return redirect(url_for('lessons.view_body', lesson_id=body.lesson_id))
    elif request.method == 'GET':
        form.question.data = body.question
        form.answers.data = body.answers
        form.lesson_id.data = body.lesson_id 
    return render_template('update_body.html', title='Update Questions and Answers', body=body, form=form)


@lessons_bp.route('/lesson/<int:lesson_id>/delete ', methods=['GET', 'POST'])
@login_required
def delete_lesson(lesson_id):
  lesson = Lesson.query.get_or_404(lesson_id)
  if current_user.role != 'admin':
    abort(403)

  db.session.delete(lesson)
  db.session.commit()
  print('lesson deleted...')
  return redirect(url_for('lessons.lessons'))

