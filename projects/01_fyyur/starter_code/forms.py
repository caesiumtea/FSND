from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length

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
    name = StringField(
        'name', validators=[DataRequired(), Length(min=1, max=120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(min=2, max=120)]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AK', 'AK'),
            ('AL', 'AL'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MO', 'MO'),
            ('MS', 'MS'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WI', 'WI'),
            ('WV', 'WV'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired(), Length(min=10, max=120)]
    )
    phone = StringField(
        'phone', validators=[Length(min=10, max=20)]
    )
    # making image link required because the template has no option for cleanly
    # handling lack of image, and I don't want to edit the template more than
    # strictly required
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL(), Length(min=10, max=500)]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(min=10, max=120)]
    )
    website = StringField(
        'website', validators=[URL(), Length(min=10, max=120)]
    )
    seeking_talent = SelectField(
        'seeking_talent',
        choices=[
            ('True', 'Yes'),
            ('', 'No') # will be converted to boolean in app.py
            ]
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Length(min=10)],
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired(), Length(min=1, max=120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(min=2, max=120)]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AK', 'AK'),
            ('AL', 'AL'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MO', 'MO'),
            ('MS', 'MS'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WI', 'WI'),
            ('WV', 'WV'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        'phone', validators=[Length(min=10, max=20)]
    )
    # making image link required because the template has no option for cleanly
    # handling lack of image, and I don't want to edit the template more than
    # strictly required
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL(), Length(min=10, max=500)]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(min=10, max=120)]
    )
    website = StringField(
        'website', validators=[URL(), Length(min=10, max=120)]
    )
    seeking_venue = SelectField(
        'seeking_venue',
        choices=[
            ('True', 'Yes'), 
            ('', 'No') # will be converted to boolean in app.py
        ]
    )
    seeking_description = StringField(
        'seeking_description',
        validators=[Length(min=10)]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
