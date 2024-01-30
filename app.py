# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Artist, Venue, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    city_states = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
    data = []

    for city_state in city_states:
        venue_list = []
        items = Venue.query.filter_by(city=city_state.city, state=city_state.state).all()
        for venue in items:
            venue_list.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(list(filter(lambda x: x.start_time >= datetime.today(), venue.shows)))
            })
        data.append({
            "city": city_state.city,
            "state": city_state.state,
            "venues": venue_list
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    data = []
    term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(term))).all()

    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(list(filter(lambda x: x.start_time >= datetime.today(), venue.shows)))
        })

    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    past_shows = []
    upcoming_shows = []

    for show in venue.shows:
        item = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        if show.start_time < datetime.today():
            past_shows.append(item)
        else:
            upcoming_shows.append(item)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "image_link": venue.image_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
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
    form = VenueForm(request.form)

    error = False
    if form.validate():
        try:
            new_venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                website_link=form.website_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data
            )

            db.session.add(new_venue)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    if error:
        flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    else:
        flash('Venue ' + form.name.data + ' was successfully listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    message = ''
    try:
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()

    if error:
        message = 'An error occurred. Venue ' + venue_name + ' could not be deleted.'
    else:
        message = 'Venue ' + venue_name + ' was successfully deleted!'

    return message


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.with_entities(Artist.id, Artist.name).all()

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    data = []
    term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(term))).all()

    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(list(filter(lambda x: x.start_time >= datetime.today(), artist.shows)))
        })

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    past_shows = []
    upcoming_shows = []
    for show in artist.shows:
        item = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        if show.start_time < datetime.today():
            past_shows.append(item)
        else:
            upcoming_shows.append(item)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    item = Artist.query.get(artist_id)
    artist = {
        "id": item.id,
        "name": item.name,
        "genres": item.genres,
        "city": item.city,
        "state": item.state,
        "phone": item.phone,
        "website_link": item.website_link,
        "facebook_link": item.facebook_link,
        "seeking_venue": item.seeking_venue,
        "seeking_description": item.seeking_description,
        "image_link": item.image_link
    }

    form = ArtistForm(formdata=None, data=artist)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    old_name = artist.name
    form = ArtistForm(request.form)
    error = False

    if form.validate():
        try:
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = form.genres.data
            artist.facebook_link = form.facebook_link.data
            artist.website_link = form.website_link.data
            artist.image_link = form.image_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data

            db.session.add(artist)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    if error:
        flash('An error occurred. Artist ' + old_name + ' could not be updated.')

        return render_template('forms/edit_artist.html', form=form, artist=artist)
    else:
        flash('Artist ' + old_name + ' was successfully updated!')

        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    item = Venue.query.get(venue_id)

    venue = {
        "id": item.id,
        "name": item.name,
        "city": item.city,
        "state": item.state,
        "genres": item.genres,
        "address": item.address,
        "phone": item.phone,
        "image_link": item.image_link,
        "website_link": item.website_link,
        "facebook_link": item.facebook_link,
        "seeking_talent": item.seeking_talent,
        "seeking_description": item.seeking_description
    }

    form = VenueForm(formdata=None, data=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    old_name = venue.name
    form = VenueForm(request.form)
    error = False

    if form.validate():
        try:
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.genres = form.genres.data
            venue.facebook_link = form.facebook_link.data
            venue.website_link = form.website_link.data
            venue.image_link = form.image_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data

            db.session.add(venue)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    if error:
        flash('An error occurred. Venue ' + old_name + ' could not be updated.')

        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        flash('Venue ' + old_name + ' was successfully updated!')

        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)

    error = False
    if form.validate():
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                image_link=form.image_link.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                website_link=form.website_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data
            )

            db.session.add(new_artist)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    if error:
        flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    else:
        flash('Artist ' + form.name.data + ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = []

    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    error = False
    if form.validate():
        try:
            new_show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )

            db.session.add(new_show)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
    else:
        error = True

    if error:
        flash('An error occurred. Show could not be listed.')
    else:
        flash('Show was successfully listed!')

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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
