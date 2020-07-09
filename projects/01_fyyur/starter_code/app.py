#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime, timezone
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
# child of Area
# parent to Show
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  area_id = db.Column(db.Integer, db.ForeignKey("areas.id"),
    nullable=False)
  # city = db.Column(db.String(120), nullable=False)  # implemented by Area
  # state = db.Column(db.String(120), nullable=False) # implemented by Area
  genres = db.Column(db.ARRAY(db.String(60)), nullable=False)

  address = db.Column(db.String(120))
  phone = db.Column(db.String(20))
  website = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  
  image_link = db.Column(db.String(500), nullable=False)
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_desc = db.Column(db.String())

  shows = db.relationship('Show', backref='venue', lazy='joined', cascade='all, delete-orphan')

  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
# child of Area
# parent to Show
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  area_id = db.Column(db.Integer, db.ForeignKey("areas.id"),
    nullable=False)
  # city = db.Column(db.String(120), nullable=False)  # implemented by Area
  # state = db.Column(db.String(120), nullable=False) # implemented by Area
  genres = db.Column(db.ARRAY(db.String(60)), nullable=False)

  phone = db.Column(db.String(20))
  website = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))

  image_link = db.Column(db.String(500), nullable=False)
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_desc = db.Column(db.String())

  shows = db.relationship('Show', backref='artist', lazy='joined', cascade='all, delete-orphan')

  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
# child of Artist and Venue
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"),
    nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"),
    nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

class Area(db.Model):
# parent to Venue and Artist
  __tablename__ = 'areas'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  venues = db.relationship('Venue', backref='area', lazy='joined')
  artists = db.relationship('Artist', backref='area', lazy='joined')

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
# Helper functions for controllers
#  ----------------------------------------------------------------

# all time-related logic is encapsulated in the following two helper functions

# takes in an artist or venue object and returns a list of its upcoming shows.
# if the object passed is not an artist or venue, it returns None.
def getUpcoming(obj):
  result = []
  currentTime = datetime.now(timezone.utc)

  # if object is a venue, query shows by venue id
  if type(obj) == Venue:
    shows = Show.query.join(Artist).filter(Show.venue_id == obj.id,
      Show.start_time > currentTime).all() # list of Show objs
    for s in shows:
      data = {
        'artist_id': s.artist_id,
        'artist_name': s.artist.name,
        'artist_image_link': s.artist.image_link,
        'start_time': s.start_time,
      }
      result.append(data)
  # if object is an artist, query shows by artist id
  elif type(obj) == Artist:
    shows = Show.query.join(Venue).filter(Show.artist_id == obj.id,
      Show.start_time > currentTime).all() # list of Show objs
    for s in shows:
      data = {
        'venue_id': s.venue_id,
        'venue_name': s.venue.name,
        'venue_image_link': s.venue.image_link,
        'start_time': s.start_time,
      }
      result.append(data)
  else: # not an artist or venue, so return none
    return None
  return result

  # takes in an artist or venue object and returns a list of its upcoming shows.
  # if the object passed is not an artist or venue, it returns None.
def getPast(obj):
  result = []
  currentTime = datetime.now(timezone.utc)

  # if object is a venue, query shows by venue id
  if type(obj) == Venue:
    shows = Show.query.join(Artist).filter(Show.venue_id == obj.id,
      Show.start_time <= currentTime).all() # list of Show objs
    for s in shows:
      data = {
        'artist_id': s.artist_id,
        'artist_name': s.artist.name,
        'artist_image_link': s.artist.image_link,
        'start_time': s.start_time,
      }
      result.append(data)

  # if object is an artist, query shows by artist id
  elif type(obj) == Artist:
    shows = Show.query.join(Venue).filter(Show.artist_id == obj.id,
      Show.start_time <= currentTime).all() # list of Show objs
    for s in shows:
      data = {
        'venue_id': s.venue_id,
        'venue_name': s.venue.name,
        'venue_image_link': s.venue.image_link,
        'start_time': s.start_time,
      }
      result.append(data)

  else: # not an artist or venue, so return none
    return None
  return result


# search Area objects for one that matches the city and state arguments
# and return its id, or if the area doesn't exist,
def getAreaId(city, state):
  # generate query object for areas matching city and state argument
  areaQo = Area.query.filter_by(state=state, city=city)

  # if that query returns at least one object, then the city already exists  
  if areaQo.count() >= 1:
    # get the id of the area selected by the query.
    # first() is a simplification, assuming that the model will contain
    # only one area with that city/state combo. 
    return areaQo.first().id
  else:
    # query found no objects matching city and state, so it needs to be added
    newArea = Area(city=city, state=state)
    db.session.add(newArea)
    db.session.commit()
    areaId = newArea.id
    # no session.close here because it's always called from inside a function
    # that itself ends in a commit and close.
    return areaId

# takes in a venue or artist and returns a dict containing the object's id, name,
# and number of upcoming shows, as is required for a few different endpoints.
# if the function is called on something other than an artist or object, it
# returns None.
def getIdNameUpcoming(obj):
  if type(obj) == Artist or type(obj) == Venue:
    result = {
      'id': obj.id,
      'name': obj.name,
      # call helper function to get a list of upcoming shows, then get length
      # of the list to count number of shows
      'num_upcoming_shows': len(getUpcoming(obj))
    }
    return result
  else:
    return None

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  # data should be a list of "area" objects
  # each area contains city (str), state (str), and venues (list of objects)
  # each venue object contains id, name, and num_upcoming_shows

  data = []
  areas = Area.query.order_by('state').order_by('city').all()

  for a in areas: # loop through all areas
    if len(a.venues) > 0: # only show them if they contain venues
      areaData = {
      'city':  a.city,
      'state': a.state,
      'venues': []
      }
      for v in a.venues:
        # call helper function to generate a dict with just the venue data
        # needed by the response
        venueData = getIdNameUpcoming(v)
        # append to the list of venues that is stored in the areaData dict
        areaData['venues'].append(venueData)
      data.append(areaData) # add area to the result

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search}%')).all()
  count = len(venues)

  venueResult = []
  for v in venues:
    venueResult.append(getIdNameUpcoming(v))

  response = {'count': count, 'data': venueResult}

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)

  past = getPast(venue) # function returns list of past shows
  future = getUpcoming(venue) # function returns list of upcoming shows
  area = Area.query.get(venue.area_id)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": area.city,
    "state": area.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_desc,
    "image_link": venue.image_link,
    "past_shows": past,
    "upcoming_shows": future,
    "past_shows_count": len(past),
    "upcoming_shows_count": len(future)
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  name = request.form.get('name')
  
  city = request.form.get('city')
  state = request.form.get('state')
  areaId = getAreaId(city, state)

  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  imgLink = request.form.get('image_link')
  fbLink = request.form.get('facebook_link')

  try:
    newVenue = Venue(name=name, area_id=areaId, address=address, phone=phone,
      genres=genres, image_link=imgLink, facebook_link=fbLink)
    db.session.add(newVenue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + name + ' was successfully listed!')

  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('Error occurred! Venue ' + name + ' was not listed.')

  finally:
    db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
    db.session.delete(Venue.query.get(venue_id))
    db.session.commit()
    flash('Venue ' + name + ' was successfully deleted.')
  except:
    db.session.rollback()
    flash('Error occurred! Venue ' + name + ' was not deleted.')
  finally:
    db.session.close()
  return None

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  area = Area.query.get(venue.area_id)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": area.city,
    "state": area.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_desc,
    "image_link": venue.image_link
  }

  form = VenueForm(data=data)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)

  try:
    # update model object with new data from form
    venue.name = request.form.get('name')
    
    city = request.form.get('city')
    state = request.form.get('state')
    venue.area_id = getAreaId(city, state)

    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')

    venue.website = request.form.get('website')
    venue.seeking_talent = bool(request.form.get('seeking_talent'))
    venue.seeking_desc = request.form.get('seeking_description')

    # commit update
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully updated!')
  except:
    # if commit fails, roll back changes
    db.session.rollback()
    flash('Error occurred! Venue ' + venue.name + ' was not updated.')
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  data = []
  artists = Artist.query.order_by('name').all()
  
  for a in artists:
    artistData = {
      'id': a.id,
      'name': a.name
    }
    data.append(artistData)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search}%')).all()
  count = len(artists)

  artistResult = []
  for a in artists:
    artistResult.append(getIdNameUpcoming(a))

  response = {'count': count, 'data': artistResult}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  artist = Artist.query.get(artist_id)

  past = getPast(artist) # function returns list of past shows
  future = getUpcoming(artist) # function returns list of upcoming shows
  area = Area.query.get(artist.area_id)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": area.city,
    "state": area.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_desc,
    "image_link": artist.image_link,
    "past_shows": past,
    "upcoming_shows": future,
    "past_shows_count": len(past),
    "upcoming_shows_count": len(future)
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):  
  artist = Artist.query.get(artist_id)
  area = Area.query.get(artist.area_id)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": area.city,
    "state": area.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_desc,
    "image_link": artist.image_link,
  }

  form = ArtistForm(data=data)

  # TODO: populate form with fields from artist with ID <artist_id>

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  artist = Artist.query.get(artist_id)

  try:
    # update model object with new data from form
    artist.name = request.form.get('name')
    
    city = request.form.get('city')
    state = request.form.get('state')
    artist.area_id = getAreaId(city, state)

    artist.phone = request.form.get('phone')
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')

    artist.website = request.form.get('website')
    artist.seeking_venue = bool(request.form.get('seeking_venue'))
    artist.seeking_desc = request.form.get('seeking_description')
  
    # commit update
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully updated!')
  except:
    # if commit fails, roll back changes
    db.session.rollback()
    flash('Error occurred! Artist ' + artist.name + ' was not updated.')
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  name = request.form.get('name')
  
  city = request.form.get('city')
  state = request.form.get('state')
  areaId = getAreaId(city, state)

  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  imgLink = request.form.get('image_link')
  fbLink = request.form.get('facebook_link')

  try:
    newArtist = Artist(name=name, area_id=areaId, phone=phone,
      genres=genres, image_link=imgLink, facebook_link=fbLink)
    db.session.add(newArtist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + name + ' was successfully listed!')

  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('Error occurred! Artist ' + name + ' was not listed.')

  finally:
    db.session.close()

  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  shows = Show.query.order_by('id').all() #left join?
  
  for s in shows:
    artist = Artist.query.get(s.artist_id)
    showData = {
      'venue_id': s.venue_id,
      'venue_name': Venue.query.get(s.venue_id).name,
      'artist_id': s.artist_id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': s.start_time
    }
    data.append(showData)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  try:
    newShow = Show(artist_id=artist_id, venue_id=venue_id, 
      start_time=start_time)
    db.session.add(newShow)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('Error occurred! Show was not listed.')

  finally:
    db.session.close()


  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
