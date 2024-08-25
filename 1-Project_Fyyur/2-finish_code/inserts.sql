--INSERT INTO table_name (column1, column2, column3, ...)
--VALUES (value1, value2, value3, ...);

-- Venue 

-- data 1
INSERT INTO "Venue" (
    id,
    name,
    city,
    state,
    address,
    phone,
    image_link,
    facebook_link,
    genres,
    website,
    seeking_talent,
    seeking_description,
) VALUES (
    1,                            --id 
    'The Musical Hop',            --name
    'San Francisco',              --city
    'CA',                         --state
    '1015 Folsom Street',         --address
    '123-123-1234',               --phone
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',    --image_link
    'https://www.facebook.com/TheMusicalHop',  --facebook_link
    ARRAY ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],       --genres
    'https://www.themusicalhop.com',  -- website
    True,  --seeking_talent
    'We are on the lookout for a local artist to play every two weeks. Please call us.'  -- seeking_description
);

-- data 2
INSERT INTO "Venue" (
    id,
    name,
    city,
    state,
    address,
    phone,
    image_link,
    facebook_link,
    genres,
    website,
    seeking_talent
) VALUES (
    2,                                   --id
    'The Dueling Pianos Bar',            --name
    'New York',                          --city
    'NY',                                --state
    '335 Delancey Street',               --address
    '123-123-1234',                      --phone
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',    --image_link
    'https://www.facebook.com/theduelingpianos',  --facebook_link
    ARRAY ['Classical', 'R&B', 'Hip-Hop'],              --genres
    'https://www.theduelingpianos.com'           --website
);

-- data 3
INSERT INTO "Venue" (
    id,
    name,
    city,
    state,
    address,
    phone,
    image_link,
    facebook_link,
    genres,
    website,
    seeking_talent,
    past_shows_count,
    upcoming_shows_count
) VALUES (
    3,                                           --id
    'Park Square Live Music & Coffee',            --name
    'San Francisco',                              --city
    'CA',                                         --state
    '34 Whiskey Moore Ave',                       --address
    '415-000-1234',                               --phone
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',    --image_link
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',       --facebook_link
    ARRAY ['Rock n Roll', 'Jazz', 'Classical', 'Folk'],                  --genres
    'https://www.parksquarelivemusicandcoffee.com'                --website
);

  data1={
    "id: 1",
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
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }

  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }

--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------

-- Artists

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


  -- data 1
  INSERT INTO "Artist" (
      id,
      name,
      city,
      state,
      phone,
      genres,
      image_link,
      facebook_link,
      website,
      seeking_venue,
      seeking_description
  ) VALUES (
      4,                            --id
      'Guns N Petals',              --name
      'San Francisco',              --city
      'CA',                         --state
      '123-123-1234',               --phone
      ARRAY['Rock n Roll'],              --genres
      'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',    --image_link
      'https://www.facebook.com/GunsNPetals',       --facebook link
      'https://www.gunsnpetalsband.com',            --website
      True,  --seeking_venue
      'Looking for shows to perform at in the San Francisco Bay Area!'        --seeking_description
  );

  -- data 2
  INSERT INTO "Artist" (
      id,
      name,
      city,
      state,
      phone,
      genres,
      image_link,
      facebook_link,
      seeking_venue
  ) VALUES (
      5,                            --id
      'Matt Quevedo',               --name
      'New York',                   --city
      'NY',                         --state
      '300-400-5000',               --phone
      ARRAY['Jazz'],                     --genres
      'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',    --image_link
      'https://www.facebook.com/mattquevedo923251523',       --facebook link
      False  --seeking_venue
  );

  -- data 3
  INSERT INTO "Artist" (
      id,
      name,
      city,
      state,
      phone,
      genres,
      image_link,
      seeking_venue,
      past_shows_count,
      upcoming_shows_count
  ) VALUES (
      6,                                --id
      'The Wild Sax Band',              --name
      'San Francisco',                  --city
      'CA',                             --state
      '432-325-5432',                   --phone
      ARRAY['Rock n Roll'],             --genres
      'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',    --image_link
      False  --seeking_venue
  );

  data1={
    "id": 4,
    "name": 'Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }

  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }

  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }

--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------

-- Shows

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return (f"<Show ID: {self.id}\n"
    f"artist_id: {self.artist_id}\n"
    f"venue_id: {self.venue_id}\n"
    f"start_time: {self.start_time}\n")

-- data 1
 INSERT INTO "Show" (
    venue_id,
    artist_id,
    start_time
  ) VALUES (
      1,                                  --venue_id
      4,                                  --artist_id
      '2019-05-21 21:30:00.000Z'            --start_time
  );

-- data 2
  INSERT INTO "Show" (
    venue_id,
    artist_id,
    start_time
  ) VALUES (
      3,                                     --venue_id
      5,                                     --artist_id
      '2019-06-15 23:00:00.000Z'               --start_time
  );

--data 3
  INSERT INTO "Show" (
    venue_id,
    artist_id,
    start_time
  ) VALUES (
      3,                                     --venue_id
      6,                                     --artist_id
      '2035-04-01 20:00:00.000Z'               --start_time
  );

--data 4
  INSERT INTO "Show" (
    venue_id,
    artist_id,
    start_time
  ) VALUES (
      3,                                     --venue_id
      6,                                     --artist_id
      '2035-04-08 20:00:00.000Z'               --start_time
  );

--data 5
  INSERT INTO "Show" (
    venue_id,
    artist_id,
    start_time
  ) VALUES (
      3,                                     --venue_id
      6,                                     --artist_id
      '2035-04-15 20:00:00.000Z'               --start_time
  );


  data1 = {
    'venue_id': 1,
    'venue_name': 'The Musical Hop',
    'artist_id': 4,
    'artist_name': 'Guns N Petals',
    'artist_image_link': 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    'start_time': '2019-05-21T21:30:00.000Z'
  }
  
  data2 = {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 5,
    'artist_name': 'Matt Quevedo',
    'artist_image_link': 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    'start_time': '2019-06-15T23:00:00.000Z'
  }

  data3 = {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-01T20:00:00.000Z'
  }
  
  data4 = {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-08T20:00:00.000Z'
  }
  
  data5 = {
    'venue_id': 3,
    'venue_name': 'Park Square Live Music & Coffee',
    'artist_id': 6,
    'artist_name': 'The Wild Sax Band',
    'artist_image_link': 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    'start_time': '2035-04-15T20:00:00.000Z'
  }
