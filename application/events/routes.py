from flask import Blueprint
from application import  db
from flask import render_template, url_for, redirect,  request, abort, send_file 
from application.events.forms import (EventCreationForm)
from application.models import Event
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from ics import Calendar, Event as ICSEvent
from io import BytesIO
from ics.alarm import DisplayAlarm


events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['POST', 'GET'])
def events():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    # Set the number of events to display per page
    per_page = 22

    # Get the current page from the request arguments (default is page 1)
    page = request.args.get('page', 1, type=int)

    # Query to fetch events, paginated
    events = Event.query.filter_by(branch=current_user.branch).order_by(Event.event_date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    # Next and Previous page URLs for pagination
    next_url = url_for('events.events', page=events.next_num) if events.has_next else None
    prev_url = url_for('events.events', page=events.prev_num) if events.has_prev else None

    return render_template('events.html', events=events.items, title='Events', next_url=next_url, prev_url=prev_url)

@events_bp.route('/add_event', methods=['GET', 'POST'])
@login_required  
def add_event():
  form = EventCreationForm()
  if form.validate_on_submit():
     # Create a new event object
    event = Event(month=form.month.data,
                  branch = form.branch.data,
                  event_date=form.event_date.data,
                  event_desc=form.event_desc.data,
                  event_venue=form.event_venue.data,
                  event_status=form.event_status.data
                )
    db.session.add(event)
    db.session.commit()
    print('event added to the database')
    return redirect(url_for('events.add_event')) 
  return render_template('add_event.html', title='Events', form=form)


@events_bp.route('/update/<int:event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    # Logic for updating an event
    event = Event.query.get_or_404(event_id)
    form = EventCreationForm()

    if request.method == 'POST':
      event.month = request.form.get('month')
      event.event_date = datetime.strptime(request.form.get('event_date'), '%Y-%m-%d')
      event.event_desc = request.form.get('event_desc')
      event.event_venue = request.form.get('event_venue')
      event.event_status = request.form.get('event_status')

      db.session.commit()
      print('database event updated ')
      return redirect(url_for('events.events'))
    elif request.method == 'GET':
        form.month.data = event.month
        form.event_date.data = event.event_date
        form.event_desc.data = event.event_desc
        form.event_venue.data = event.event_venue
        form.event_status.data = event.event_status
 
    return render_template('update_event.html', event=event, title='Update Event', form=form)


@events_bp.route('/delete/<int:event_id>', methods=['POST', 'GET'])
def delete_event(event_id):
    # Logic for deleting an event
    event = Event.query.get_or_404(event_id)
    if current_user.role != 'admin':
      abort(403)

    db.session.delete(event)
    db.session.commit()
    print('Event deleted...')
    return redirect(url_for('events.events'))


@events_bp.route('/general_events', methods=['POST', 'GET'])
def general_events():
  # query to fetch al events from the database
  if current_user.is_authenticated:
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date.desc()).paginate(page=page, per_page=10)
  else:
     return redirect(url_for('events.login'))

  return render_template('general_events.html', events=events, title='Events')

@events_bp.route('/get_event/<int:event_id>', methods=['GET'])
def get_event(event_id):
  event = Event.query.filter_by(id=event_id).first()

  if event:
       # event details to search for
      event_details = {
        "event_date": event.event_date,  # datetime object
        "event_desc": event.event_desc,
        "event_venue": event.event_venue,
        "event_status": event.event_status,
  }    
  return render_template("event_detail.html", event=event_details)
     

@events_bp.route('/download_ics/<int:event_id>', methods=['GET'])
def download_ics(event_id):
    # Fetch event details from the database using the provided event_id
    show_event = Event.query.filter_by(id=event_id).first()

    if show_event:
        # Create the event details for ICS conversion
        event_details = {
            "event_date": show_event.event_date,  # assuming event_date is a datetime object
            "event_desc": show_event.event_desc,
            "event_venue": show_event.event_venue,
            "event_status": show_event.event_status,
        }

        # Create an ICS event
        cal = Calendar()
        ics_event = ICSEvent()
        ics_event.name = event_details["event_desc"]
        ics_event.begin = event_details["event_date"]
        ics_event.location = event_details["event_venue"]
        ics_event.description = event_details["event_desc"]

        

        # Add  alarm / reminders
        one_week_reminder = DisplayAlarm(trigger=timedelta(hours=-132))  # 1-week reminder before the event
        one_day_reminder = DisplayAlarm(trigger=timedelta(hours=-20))
        twelve_hour_reminder = DisplayAlarm(trigger=timedelta(hours=-12))

        # Attach the alarms to the event
        ics_event.alarms.append(one_day_reminder)
        ics_event.alarms.append(one_week_reminder)
        ics_event.alarms.append(twelve_hour_reminder)

        cal.events.add(ics_event)

        # Write the ICS file to a buffer
        buffer = BytesIO()
        buffer.write(str(cal).encode("utf-8"))
        buffer.seek(0)

        # Return the file as a download
        filename = f"{event_details['event_desc'].replace(' ', '_')}.ics"
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype="text/calendar")
    
    # If event not found
    return "Event not found", 404