from flask import Blueprint
from flask_login import current_user, login_required
from flask import render_template, url_for, redirect, request, abort
from application.announcements.forms import (CreateAnnouncementForm,UpdateAnnouncementForm )
from application.models import Announcement

from application import db


announcements_bp = Blueprint('announcements', __name__)

## Announcements
@announcements_bp.route('/announcements/schedule', methods=['GET'])
@login_required  
def sabbath_schedule():
  return render_template('sabbath_schedule.html', title='Sabbath Schedule')
 
@announcements_bp.route('/announcements')
def announcements():
    # Ensure the user is authenticated
    if not current_user.is_authenticated:
        abort(403)

    # Filter announcements based on the current user's branch
    user_branch = current_user.branch  # Get the user's branch
    page = request.args.get('page', 1, type=int)
    
    # Query the database for announcements specific to the user's branch
    announcements = Announcement.query.filter_by(branch=user_branch)\
                                      .order_by(Announcement.date_posted.desc())\
                                      .paginate(page=page, per_page=15)
    
    return render_template('announcements.html', title='Announcements', announcements=announcements)



@announcements_bp.route('/announcement/new ', methods=['GET', 'POST'])
@login_required
def create_announcement():
  form = CreateAnnouncementForm()
  if form.validate_on_submit():
    announcement =Announcement(title=form.title.data,branch=form.branch.data, content=form.content.data, author=current_user)
    db.session.add(announcement)
    db.session.commit()
    print('Added to the db')
    return redirect(url_for('announcements.announcements'))
  else:
    print("failed to add announcement")
  return render_template('create_announcement.html', title='New Announcement' , form=form)

@announcements_bp.route('/announcement/<int:announcement_id> ', methods=['GET', 'POST'])
@login_required
def show_announcement(announcement_id):
   announcement = Announcement.query.get_or_404(announcement_id)
   return render_template('show_announcement.html', title='Announcement', announcement=announcement)


@announcements_bp.route('/announcement/<int:announcement_id>/update ', methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
  announcement = Announcement.query.get_or_404(announcement_id)
  form = UpdateAnnouncementForm()
  if announcement.author != current_user:
     abort(403)

  if form.validate_on_submit():
    announcement.title = form.title.data
    announcement.branch = form.announcement.data
    announcement.content = form.content.data
    db.session.commit()
    db.session.refresh(announcement)
    print('update successful')
    return redirect(url_for('announcements.show_announcement', announcement_id=announcement.id))
  elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
        
  return render_template('create_announcement.html', title='Update nnouncement', form=form, announcement=announcement)

@announcements_bp.route('/announcement/<int:announcement_id>/delete ', methods=['GET', 'POST'])
@login_required
def delete_announcement(announcement_id):
  announcement = Announcement.query.get_or_404(announcement_id)
  if announcement.author != current_user:
    abort(403)

  db.session.delete(announcement)
  db.session.commit()
  print(f'Deleted')
  return redirect(url_for('announcements.announcements'))

@announcements_bp.route('/general_announcements')
def general_announcements():
    # Ensure the user is authenticated
    if not current_user.is_authenticated:
        abort(403)
    page = request.args.get('page', 1, type=int)    
  # Query the database for all announcements
    announcements=Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('general_announcements.html', title='Announcements', announcements=announcements)

    