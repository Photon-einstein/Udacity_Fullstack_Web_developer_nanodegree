#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import dateutil.parser
import babel
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
from sqlalchemy.sql.expression import func

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app) # just initiate here
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
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


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venue_locations = Venue.query.order_by(Venue.state, Venue.city).all()
  for venue_location in venue_locations:
    venue_location_data_set = venue_location.query.filter_by(state=venue_location.state).filter_by(city=venue_location.city).all()
    venue_data_per_location = []
    for venue_location_data in venue_location_data_set:
      venue_data_per_location.append({
        'id': venue_location_data.id,
        'name': venue_location_data.name,
        'num_upcoming_shows': len(db.session.query(Show).filter(Show.venue_id==venue_location_data.id).filter(Show.start_time > datetime.now()).all())
      })

    data.append({
      'city': venue_location.city,
      'state': venue_location.state,
      'venues': venue_data_per_location
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term', '')
  search_result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  response = []
  matches = []
  for venue in search_result:
    matches.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': len(db.session.query(Show).filter(Show.venue_id==venue.id).filter(Show.start_time > datetime.now()).all())
    })

  response = {
     'count': len(search_result),
     'data': matches
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()

  shows = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).all()
  past_shows = []
  upcoming_shows = []
  for show in shows:
    show_info = {
        'artist_id': show.artist_id,
        'artist_name': show.Artist.name,  # Accessing the Artist name
        'artist_image_link': show.Artist.image_link,  # Accessing the Artist image link
        'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    start_time = datetime.strptime(show_info['start_time'], '%Y-%m-%d %H:%M:%S')
    if start_time <= datetime.now():
      past_shows.append(show_info)
    else:
      upcoming_shows.append(show_info)

  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
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
  error = False
  # Set the FlaskForm
  form = VenueForm(request.form, meta={'csrf':False})
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  # Validate all fields
  if form.validate():
    # Prepare for transaction
    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        genres = form.genres.data
        website = form.website_link.data
        if form.seeking_talent.data == 'y':
          seeking_talent = True
        else:
          seeking_talent = False
        seeking_description = form.seeking_description.data

        venue = Venue(name=name, 
                      city=city,
                      state=state,
                      address=address,
                      phone=phone,
                      image_link=image_link,
                      facebook_link=facebook_link,
                      genres=genres,
                      website=website,
                      seeking_description=seeking_description
        )
        venue.seeking_talent = seeking_talent
        db.session.add(venue)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html', form=venue)
  else:
    message = []
    for field, errors in form.errors.items():
      for error in errors:
        message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('pages/home.html', form=form)
     

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  if request.form.get('_method') == 'DELETE':
    error = False
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        if venue is None:
          flash('Venue with id ' + str(venue_id) + ' does not exist.')
          return redirect(url_for('pages/home.html'))
        
        db.session.delete(venue)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = True
        print(f"Error occurred: {e}")  # Log the exception for debugging
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue with id' + str(venue_id) + ' could not be deleted.')
    else:
        flash('Venue with id '+ str(venue_id) +' sucessfully deleted.')

    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artist_data_set = Artist.query.order_by(Artist.id, Artist.name).all()
  for artist_data in artist_data_set:
     data.append({
        'id': artist_data.id,
        'name': artist_data.name
     })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term', '')
  search_result = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  response = []
  matches = []
  for artist in search_result:
    matches.append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': len(db.session.query(Show).filter(Show.artist_id==artist.id).filter(Show.start_time > datetime.now()).all())
    })

  response = {
     'count': len(search_result),
     'data': matches
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first()

  shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).all()
  past_shows = []
  upcoming_shows = []
  for show in shows:
    show_info = {
        'venue_id': show.venue_id,
        'venue_name': show.Venue.name,  # Accessing the Venue name
        'venue_image_link': show.Venue.image_link,  # Accessing the Venue image link
        'start_time': show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    start_time = datetime.strptime(show_info['start_time'], '%Y-%m-%d %H:%M:%S')
    if start_time <= datetime.now():
      past_shows.append(show_info)
    else:
      upcoming_shows.append(show_info)

  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  if artist:
     form.name.data = artist.name
     form.genres.data = artist.genres
     form.city.data = artist.city
     form.state.data = artist.state
     form.phone.data = artist.phone
     form.website_link.data = artist.website
     form.facebook_link.data = artist.facebook_link
     form.seeking_venue.data = artist.seeking_venue
     form.seeking_description.data = artist.seeking_description
     form.image_link.data = artist.image_link

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
   # Set the FlaskForm
  form = ArtistForm(request.form, meta={'csrf':False})
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  # Validate all fields
  if form.validate():
    # Prepare for transaction
    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        if form.seeking_venue.data == 'y':
          artist.seeking_venue = True
        else:
          artist.seeking_venue = False
        artist.seeking_description = form.seeking_description.data    
        artist.image_link = form.image_link.data

        db.session.add(artist)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = True
        print(f"Error occurred: {e}")  # Log the exception for debugging
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist with id' + artist_id + ' could not be updated.')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    message = []
    for field, errors in form.errors.items():
      for error in errors:
        message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = ArtistForm()
    return render_template('pages/home.html', form=form)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.filter_by(id=venue_id).first()
  if  venue is not None:
     form.name.data = venue.name
     form.genres.data = venue.genres
     form.address.data = venue.address
     form.city.data = venue.city
     form.state.data = venue.state
     form.phone.data = venue.phone
     form.website_link.data = venue.website
     form.facebook_link.data = venue.facebook_link
     form.seeking_talent.data = venue.seeking_talent
     form.seeking_description.data = venue.seeking_description
     form.image_link.data = venue.image_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
   # Set the FlaskForm
  form = VenueForm(request.form, meta={'csrf':False})
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  # Validate all fields
  if form.validate():
    # Prepare for transaction
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.address = form.address.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.website = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        if form.seeking_talent.data == 'y':
          venue.seeking_talent = True
        else:
          venue.seeking_talent = False
        venue.seeking_description = form.seeking_description.data    
        venue.image_link = form.image_link.data

        db.session.add(venue)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = True
        print(f"Error occurred: {e}")  # Log the exception for debugging
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue with id' + str(venue_id) + ' could not be updated.')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    message = []
    for field, errors in form.errors.items():
      for error in errors:
        message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('pages/home.html', form=form)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  # Set the FlaskForm
  form = ArtistForm(request.form, meta={'csrf':False})
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  # Validate all fields
  if form.validate():
    # Prepare for transaction
    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = form.genres.data
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website = form.website_link.data
        if form.seeking_venue.data == 'y':
          seeking_venue = True
        else:
          seeking_venue = False
        seeking_description = form.seeking_description.data

        artist = Artist(name=name, 
                        city=city,
                        state=state,
                        phone=phone,
                        genres=genres,
                        image_link=image_link,
                        facebook_link=facebook_link,
                        website=website,
                        seeking_venue=seeking_venue,
                        seeking_description=seeking_description)
        
        db.session.add(artist)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  else:
    message = []
    for field, errors in form.errors.items():
      for error in errors:
        message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = ArtistForm()
    return render_template('pages/home.html', form=form)


@app.route('/artists/<artist_id>', methods=['POST'])
def delete_artist(artist_id):
  # Test with: $ curl -X DELETE http://localhost:5000/artists/<id>, venue shoud not be linked with Show database
  if request.form.get('_method') == 'DELETE':
    error = False
    try:
        artist = Artist.query.filter_by(id=artist_id).first()
        if artist is None:
          flash('Artist with id ' + str(artist_id) + ' does not exist.')
          return redirect(url_for('pages/home.html'))
        
        db.session.delete(artist)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error = True
        print(f"Error occurred: {e}")  # Log the exception for debugging
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist with id' + str(artist_id) + ' could not be deleted.')
    else:
        flash('Artist with id '+ str(artist_id) +' sucessfully deleted.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  all_shows_expanded = db.session.query(Show).join(Artist).join(Venue).all()
  print(all_shows_expanded)
  data = []

  for show_expanded in all_shows_expanded:
    data.append({
        'venue_id': show_expanded.venue_id,
        'venue_name': show_expanded.Venue.name,  # Accessing the Venue name
        'artist_id': show_expanded.artist_id,
        'artist_name': show_expanded.Artist.name,  # Accessing the Artist name
        'artist_image_link': show_expanded.Artist.image_link,  # Accessing the Artist image link
        'start_time': show_expanded.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  # Set the FlaskForm
  form = ShowForm(request.form, meta={'csrf':False})
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  # Validate all fields
  if form.validate():
    try:
        artist_id = form.artist_id.data
        venue_id = form.venue_id.data
        start_time = form.start_time.data

        show = Show(artist_id=artist_id,
                    venue_id=venue_id,
                    start_time=start_time)
        
        db.session.add(show)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('Show was successfully listed!')
    return render_template('pages/home.html')
  else:
    message = []
    for field, errors in form.errors.items():
      for error in errors:
        message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = ShowForm()
    return render_template('pages/home.html', form=form)

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
