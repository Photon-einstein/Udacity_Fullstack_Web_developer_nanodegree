from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import DateTimeField, StringField, SelectField, SelectMultipleField, BooleanField,  ValidationError
from wtforms.validators import DataRequired, URL, Regexp
from enums import *
import re

def is_valid_phone(number):
    """ Validate phone numbers like:
    1234567890    - no space
    123.456.7890  - dot separator
    123-456-7890  - dash separator
    123 456 7890  - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -. = ?[-. ] 
    
    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})')
    return regex.match(number)

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):

    def validate_phone(self, field):
        if not is_valid_phone(field.data):
            raise ValidationError('Invalid phone.')
    
    def validate_genres(self, field):
        if not set(field.data).issubset(dict(Genres.choices()).keys()):
            raise ValidationError('Invalid genres.')

    def validate_state(self, field):
        if field.data not in dict(States.choices()).keys():
            raise ValidationError('Invalid state.')
    
    def validate(self, **kwargs):
        # **kwargs to match the method's signature in the 'FlaskForm' class
        return super(VenueForm, self).validate(**kwargs)

    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.choices()
    )

    address = StringField(
        'address', validators=[DataRequired()]
    )

    phone = StringField(
        'phone', validators=[DataRequired()]
    )

    image_link = StringField(
        'image_link'
    )

    genres = SelectMultipleField(
                'genres', 
                validators=[DataRequired()],
                choices=Genres.choices()
            )

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    website_link = StringField(
        'website'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(Form):

    def validate_phone(self, field):
        if not is_valid_phone(field.data):
            raise ValidationError('Invalid phone.')
    
    def validate_genres(self, field):
        if not set(field.data).issubset(dict(Genres.choices()).keys()):
            raise ValidationError('Invalid genres.')

    def validate_state(self, field):
        if field.data not in dict(States.choices()).keys():
            raise ValidationError('Invalid state.')
    
    def validate(self, **kwargs):
        # **kwargs to match the method's signature in the 'FlaskForm' class
        return super(ArtistForm, self).validate(**kwargs)

    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=States.choices()
    )
    
    phone = StringField(
        'phone'
    )

    image_link = StringField(
        'image_link'
    )

    genres = SelectMultipleField(
                'genres', 
                validators=[DataRequired()],
                choices=Genres.choices()
            )

    facebook_link = StringField(
        'facebook_link'
     )
       
    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )
