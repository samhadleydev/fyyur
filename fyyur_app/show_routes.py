#____________________________________________________________________________________
#                                                                             IMPORTS
from fyyur_app import app, db, format_datetime
from fyyur_app.models import *
from fyyur_app.forms import *
from flask import render_template, request, flash, redirect, url_for
#____________________________________________________________________________________
#                                                                              ROUTES
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.

    data = []

    shows = Show.query.all()
    
    for show in shows:
        data.append({
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
        })
        
    return render_template(
        'pages/shows.html',
        shows=data)
#____________________________________________________________________________________
#                                                                         Create Show
@app.route('/shows/create')
def create_shows():

    form = ShowForm()

    return render_template(
        'forms/new_show.html',
        form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    form = ShowForm(request.form)

    venue_id = form.venue_id.data,
    artist_id = form.artist_id.data,
    start_time = form.start_time.data

    new_show = Show(
        venue_id=venue_id,
        artist_id=artist_id,
        start_time=start_time
    )
    try:
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed. You\'re on Fyyur!')
    except:
        flash('Oops! Something went wrong: Show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

  # DONE: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.