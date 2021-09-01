from fyyur_app import app, db, datetime
from fyyur_app.models import *
from fyyur_app.forms import *
from flask import render_template, request, flash, redirect, url_for


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database

  data=[]

  artists = db.session.query(Artist.id, Artist.name)
  for artist in artists:
      data.append({
        "id": artist[0],
        "name": artist[1]
      })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '').strip()
  # .ilike is case insensitive, % wildcards added
  # db.session.query(Model) is callible

  artists = db.session.query(Artist).filter(Artist.name.ilike('%' + search_term + '%')).all()

  data = []

  for artist in artists:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter_by(artist_id=artist.id).all()
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

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get(artist_id)
  # single line loop to get genre data from relational table

  genres = [ genre.name for genre in artist.genres ]

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

  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

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
      flash('Oops! Something went wrong. ' + artist_name + ' could not be added.')
  finally:
      db.session.close()
  return render_template('pages/home.html')

  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):

  artist = Artist.query.get(artist_id)
  try:
    db.session.delete(artist)
    db.session.commit()
    flash('Artist successfully deleted.')
  except:
    flash('Oops! Something went wrong. Artist could not be deleted.')
  finally:
    db.session.close()
  return redirect(url_for('index'))

  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
