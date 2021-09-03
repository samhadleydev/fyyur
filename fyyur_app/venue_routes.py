from fyyur_app import app, db, datetime
from fyyur_app.models import *
from fyyur_app.forms import *

from flask import render_template, request, flash, redirect, url_for



@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data=[]

  locations = db.session.query(Venue.city, Venue.state)

  for location in locations:
      venues = db.session.query(
                      Venue.id, Venue.name).filter(
                      Venue.city == location[0]).filter(
                      Venue.state == location[1])
      data.append({
        "city": location[0],
        "state": location[1],
        "venues": venues
      })


  # DONE: replace with real venues data.

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '').strip()
  # .ilike is case insensitive, % wildcards added
  # db.session.query(Model) is callible
  venues = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term + '%')).all()

  data = []

  for venue in venues:
    num_upcoming_shows = 0
    shows = db.session.query(Show).filter_by(venue_id=venue.id).all()
    for show in shows:
            if show.start_time > datetime.now():
                num_upcoming_shows += 1;
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_shows
    })

  # DONE: implement search on venues with partial string search. Ensure it is case-insensitive.

  response={
    "count": len(venues),
    "data": data
    }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  
  venue = Venue.query.get(venue_id)
  # single line loop to get genre data from relational table
  genres = [ genre.name for genre in venue.genres ]

  upcoming_shows = []
  past_shows = []

  for show in venue.shows:
    if show.start_time > datetime.now:
      upcoming_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%m/%d/%Y')
    })
      if show.start_time < datetime.now:
        past_shows.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%m/%d/%Y')
      })

  data = {
      "id": venue.id,
      "name": venue.name,
      "genres": genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website_link": venue.website_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "upcoming_shows": upcoming_shows,
      "upcoming_shows_count": len(upcoming_shows),
      "past_shows": past_shows,
      "past_shows_count": len(past_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()

  name = form.name.data
  address = form.address.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  website_link = form.website_link.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  seeking_talent = form.seeking_talent.data
  seeking_description = form.seeking_description.data
  genres = form.genres.data

  venue_name = request.form['name']

  new_venue = Venue(
    name=name,
    city=city, 
    state=state, 
    address=address, 
    phone=phone,
    seeking_talent=seeking_talent, 
    seeking_description=seeking_description, 
    image_link=image_link,
    website_link=website_link, 
    facebook_link=facebook_link
    )
  for genre in genres:
    get_genre = Genre.query.filter_by(name=genre).one_or_none()
    if get_genre:
        new_venue.genres.append(get_genre)

    else:
        new_genre = Genre(name=genre)
        db.session.add(new_genre)
        new_venue.genres.append(new_genre)

  try:
      db.session.add(new_venue)
      db.session.commit()
      flash(venue_name + ' was successfully listed. You\'re on Fyyur!')
  except:
      flash('Oops! Something went wrong. ' + venue_name + ' could not be added.')
  finally:
      db.session.close()
  return render_template('pages/home.html')

  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):

  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue successfully deleted.')
  except:
    flash('Oops! Something went wrong. Venue could not be deleted.')
  finally:
    db.session.close()
  return redirect(url_for('index'))

  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)



  name = form.name.data
  address = form.address.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  website_link = form.website_link.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  seeking_talent = form.seeking_talent.data
  seeking_description = form.seeking_description.data
  genres = form.genres.data

  updated_venue = Venue(
    name=name,
    city=city, 
    state=state, 
    address=address, 
    phone=phone,
    seeking_talent=seeking_talent, 
    seeking_description=seeking_description, 
    image_link=image_link,
    website_link=website_link, 
    facebook_link=facebook_link
    )

  venue.genres = []

  for genre in genres:
    get_genre = Genre.query.filter_by(name=genre).one_or_none()
    if get_genre:
        venue.genres.append(get_genre)

    else:
        new_genre = Genre(name=genre)
        db.session.add(new_genre)
        venue.genres.append(new_genre)

  try:
      db.session.commit()
      flash('Update successful. You\'re on Fyyur!')
  except:
      flash('Oops! Something went wrong: Update unsuccessful.')
  finally:
      db.session.close()


  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))
