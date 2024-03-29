# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime

db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=True)
    seeking_description = db.Column(
        db.String(500),
        default='We are on the lookout for a local artist to play every two weeks. Please call us.'
    )

    def add(self):
        db.session.add(self)
        db.session.commit()

    def revert():
        db.session.rollback()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Venue %r>' % self

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'genres': self.genres.split(','),
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'address': self.address,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'website': self.website,
                'seeking_talent': self.seeking_talent,
                'seeking_description': self.seeking_description
                }

    @property
    def serialize_with_upcoming_shows_count(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'address': self.address,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'website': self.website,
                'seeking_talent': self.seeking_talent,
                'seeking_description': self.seeking_description,
                'num_of_shows': Shows.query.filter(
                    Shows.start_time > datetime.datetime.now(),
                    Shows.venue_id == self.id)
                }

    @property
    def serialize_with_shows_details(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'address': self.address,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'seeking_talent': self.seeking_talent,
                'seeking_description': self.seeking_description,
                'website': self.website,
                'upcoming_shows': [show.serialize_with_artist_venue for show in Shows.query.filter(
                    Shows.start_time > datetime.datetime.now(),
                    Shows.venue_id == self.id).all()],
                'past_shows': [show.serialize_with_artist_venue for show in Shows.query.filter(
                    Shows.start_time < datetime.datetime.now(),
                    Shows.venue_id == self.id).all()],
                'upcoming_shows_count': len(Shows.query.filter(
                    Shows.start_time > datetime.datetime.now(),
                    Shows.venue_id == self.id).all()),
                'past_shows_count': len(Shows.query.filter(
                    Shows.start_time < datetime.datetime.now(),
                    Shows.venue_id == self.id).all())
                }

    @property
    def filter_on_city_state(self):
        return {'city': self.city,
                'state': self.state,
                'venues': [v.serialize_with_upcoming_shows_count
                           for v in Venue.query.filter(Venue.city == self.city,
                                                       Venue.state == self.state).all()]}


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def revert():
        db.session.rollback()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Artist %r>' % self

    @property
    def serialize_with_shows_details(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'genres': self.genres,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                'upcoming_shows': [show.serialize_with_artist_venue for show in Shows.query.filter(
                    Shows.start_time > datetime.datetime.now(),
                    Shows.artist_id == self.id).all()],
                'past_shows': [show.serialize_with_artist_venue for show in Shows.query.filter(
                    Shows.start_time < datetime.datetime.now(),
                    Shows.artist_id == self.id).all()],
                'upcoming_shows_count': len(Shows.query.filter(
                    Shows.start_time > datetime.datetime.now(),
                    Shows.artist_id == self.id).all()),
                'past_shows_count': len(Shows.query.filter(
                    Shows.start_time < datetime.datetime.now(),
                    Shows.artist_id == self.id).all())
                }

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'city': self.city,
                'state': self.state,
                'phone': self.phone,
                'genres': self.genres,
                'image_link': self.image_link,
                'facebook_link': self.facebook_link,
                }


class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime(), server_default=db.func.current_timestamp())

    def add(self):
        db.session.add(self)
        db.session.commit()

    def revert():
        db.session.rollback()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Show %r>' % self

    @property
    def serialize(self):
        return {'id': self.id,
                'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                'venue_id': self.venue_id,
                'artist_id': self.artist_id
                }

    @property
    def serialize_with_artist_venue(self):
        return {'id': self.id,
                'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
                'venue': [v.serialize for v in Venue.query.filter(Venue.id == self.venue_id).all()][0],
                'artist': [a.serialize for a in Artist.query.filter(Artist.id == self.artist_id).all()][0]
                }
