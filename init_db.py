import datetime

from models import *

venue1 = Venue(name='The Musical Hop',
               city='San Francisco',
               state='CA',
               address='1015 Folsom Street',
               phone='123-123-1234',
               image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1'
                          '.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
               genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"],
               facebook_link='https://www.facebook.com/TheMusicalHop',
               website_link='https://www.themusicalhop.com',
               seeking_talent=True,
               seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.')

venue2 = Venue(name='The Dueling Pianos Bar',
               city='New York',
               state='NY',
               address='335 Delancey Street',
               phone='914-003-1132',
               image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid'
                          '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
               genres=["Classical", "R&B", "Hip-Hop"],
               facebook_link='https://www.facebook.com/theduelingpianos',
               website_link='https://www.theduelingpianos.com',
               seeking_talent=False,
               seeking_description='')

venue3 = Venue(name='Park Square Live Music & Coffee',
               city='San Francisco',
               state='CA',
               address='34 Whiskey Moore Ave',
               phone='415-000-1234',
               image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid'
                          '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
               genres=["Rock n Roll", "Jazz", "Classical", "Folk"],
               facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
               website_link='https://www.parksquarelivemusicandcoffee.com',
               seeking_talent=False,
               seeking_description='')

artist1 = Artist(name='Guns N Petals',
                 city='San Francisco',
                 state='CA',
                 phone='326-123-5000',
                 image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid'
                            '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
                 genres=["Rock n Roll"],
                 facebook_link='https://www.facebook.com/GunsNPetals',
                 website_link='https://www.gunsnpetalsband.com',
                 seeking_venue=True,
                 seeking_description='Looking for shows to perform at in the San Francisco Bay Area!')

artist2 = Artist(name='Matt Quevedo',
                 city='New York',
                 state='NY',
                 phone='300-400-5000',
                 image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid'
                            '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
                 genres=["Jazz"],
                 facebook_link='https://www.facebook.com/mattquevedo923251523',
                 website_link='',
                 seeking_venue=False,
                 seeking_description='')

artist3 = Artist(name='The Wild Sax Band',
                 city='San Francisco',
                 state='CA',
                 phone='432-325-5432',
                 image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid'
                            '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
                 genres=["Jazz", "Classical"],
                 facebook_link='',
                 website_link='',
                 seeking_venue=False,
                 seeking_description='')

show1 = Show(artist=artist1, venue=venue1, start_time=datetime.datetime.strptime('2019-05-21T21:30:00.000Z',
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'))
show2 = Show(artist=artist2, venue=venue3, start_time=datetime.datetime.strptime('2019-06-15T23:00:00.000Z',
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'))
show3 = Show(artist=artist3, venue=venue3, start_time=datetime.datetime.strptime('2035-04-01T20:00:00.000Z',
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'))
show4 = Show(artist=artist3, venue=venue3, start_time=datetime.datetime.strptime('2035-04-08T20:00:00.000Z',
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'))
show5 = Show(artist=artist3, venue=venue3, start_time=datetime.datetime.strptime('2035-04-15T20:00:00.000Z',
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'))

try:
    db.session.add_all([artist1, artist2, artist3])
    db.session.add_all([venue1, venue2, venue3])
    db.session.add_all([show1, show2, show3, show4, show5])
    db.session.commit()
except:
    db.session.rollback()
finally:
    db.session.close()
