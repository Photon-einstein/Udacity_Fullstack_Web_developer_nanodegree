from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
  
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(400))
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
      return (f"<Venue ID: {self.id}\n"
      f"name: {self.name}\n"
      f"city: {self.city}\n"
      f"state: {self.state}\n"
      f"address: {self.address}\n"
      f"phone: {self.phone}>\n"
      f"image_link: {self.image_link}\n"
      f"facebook_link: {self.facebook_link}\n"
      f"genres: {self.genres}\n"
      f"website: {self.website}\n"
      f"seeking_talent: {self.seeking_talent}\n"
      f"seeking_description: {self.seeking_description}\n")

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(250))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    def __repr__(self):
      return (f"<Artist ID: {self.id}\n"
      f"name: {self.name}\n"
      f"city: {self.city}\n"
      f"state: {self.state}\n"
      f"phone: {self.phone}\n"
      f"genres: {self.genres}\n"
      f"image_link: {self.image_link}\n"
      f"facebook_link: {self.facebook_link}\n"
      f"website: {self.website}\n"
      f"seeking_venue: {self.seeking_venue}\n"
      f"seeking_description: {self.seeking_description}\n")

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return (f"<Show ID: {self.id}\n"
    f"artist_id: {self.artist_id}\n"
    f"venue_id: {self.venue_id}\n"
    f"start_time: {self.start_time}\n")
