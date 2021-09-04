#____________________________________________________________________________________
#                                                                             IMPORTS
from fyyur_app import app, db, datetime
from fyyur_app.models import *
from fyyur_app.forms import *
from flask import render_template, request, flash, redirect, url_for
#____________________________________________________________________________________
#                                                                              ROUTES
@app.route('/artists')
def artists():

  # DONE: replace with real data returned from querying the database

    data=[]

    artists = db.session.query(
                Artist.id,
                Artist.name
                )

    for artist in artists:
        data.append({
            "id": artist[0],
            "name": artist[1]
        })

    return render_template(
        'pages/artists.html',
        artists=data)
#____________________________________________________________________________________
#                                                                      Search Artists
@app.route('/artists/search', methods=['POST'])
def search_artists():

    search_term = request.form.get('search_term', '').strip()

    artists = db.session.query(
                Artist).filter(
                Artist.name.ilike(
                '%' + search_term + '%')).all()
    
    # .ilike is case insensitive, % wildcards added
    # db.session.query(Model) is callible

    data = []

    for artist in artists:

        num_upcoming_shows = 0

        shows = db.session.query(
                Show).filter_by(
                artist_id=artist.id).all()

        for show in shows:
            if show.start_time > datetime.now():
                num_upcoming_shows += 1;

    data.append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": num_upcoming_shows
    })

  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.

    response={
        "count": len(artists),
        "data": data
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', ''))
#____________________________________________________________________________________
#                                                                         Show Artist
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get(artist_id)

    genres = [ genre.name for genre in artist.genres ]
    # single line loop to get genre data from relational table

    upcoming_shows = []

    past_shows = []

    for show in artist.shows:
        if show.start_time > datetime.now:
                upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y')
            })
        if show.start_time < datetime.now:
            past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y')
            })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),
    }

    return render_template(
        'pages/show_artist.html', 
        artist=data)
#____________________________________________________________________________________
#                                                                       Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():

    form = ArtistForm()

    return render_template(
        'forms/new_artist.html',
        form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    form = ArtistForm()

    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    website_link = form.website_link.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    seeking_venue = form.seeking_venue.data
    seeking_description = form.seeking_description.data
    genres = form.genres.data

    artist_name = request.form['name']

    new_artist = Artist(
        name=name,
        city=city, 
        state=state, 
        phone=phone,
        seeking_venue=seeking_venue, 
        seeking_description=seeking_description, 
        image_link=image_link,
        website_link=website_link, 
        facebook_link=facebook_link
    )

    for genre in genres:
        get_genre = Genre.query.filter_by(name=genre).one_or_none()
        if get_genre:
            new_artist.genres.append(get_genre)
        else:
            new_genre = Genre(name=genre)
            db.session.add(new_genre)
            new_artist.genres.append(new_genre)

    try:
        db.session.add(new_artist)
        db.session.commit()
        flash(artist_name + ' was successfully listed. You\'re on Fyyur!')
    except:
        flash('Oops! Something went wrong. ' + artist_name + ' could not be listed.')
    finally:
        db.session.close()
    return render_template(
        'pages/home.html')

  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
#____________________________________________________________________________________
#                                                                         Edit Artist
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    artist = Artist.query.get(artist_id)

    form = ArtistForm(obj=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    form = ArtistForm(request.form)

    artist = Artist.query.get(artist_id)

    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.website_link = request.form['website_link']
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_description = request.form['seeking_description']
    db.session.add(artist)

    artist.genres.clear()
    genres = form.genres.data
  
    for genre in genres:
        get_genre = Genre.query.filter_by(name=genre).one_or_none()
        if get_genre:
            artist.genres.append(get_genre)
        else:
            new_genre = Genre(name=genre)
            db.session.add(new_genre)
            artist.genres.append(new_genre)

    try:
        db.session.commit()
        flash('Update successful. You\'re on Fyyur!')
    except:
        flash('Oops! Something went wrong: Update unsuccessful.')
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))

  # DONE: populate form with fields from artist with ID <artist_id>
#____________________________________________________________________________________
#                                                                       Delete Artist
@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):

    artist = Artist.query.get(artist_id)

    try:
        db.session.delete(artist)
        db.session.commit()
        flash('Artist successfully deleted.')
    except:
        flash('Oops! Something went wrong: Artist could not be deleted.')
    finally:
        db.session.close()
    return redirect(url_for('index'))

  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion