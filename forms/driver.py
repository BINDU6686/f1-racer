
from wtforms import Form, SelectField, StringField, validators, IntegerField, FloatField

# class RegistrationForm(Form):
#     username     = StringField('Username', [validators.Length(min=4, max=25)])
#     email        = StringField('Email Address', [validators.Length(min=6, max=35)])
#     accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])\
        
        

class DriverForm(Form):
    driver_name = StringField('Driver name', )
    age = IntegerField("Age", [validators.NumberRange(min=18), validators.InputRequired('Input is mandatory.')])
    total_pole_position = IntegerField("Total pole position", [validators.NumberRange(min=0), validators.InputRequired('Input is mandatory.')])
    total_race_wins = IntegerField("Total race wins", [validators.NumberRange(min=10), validators.InputRequired('Input is mandatory.')])
    total_points_scored = FloatField("Total points scored", [validators.NumberRange(min=0.0), validators.InputRequired('Input is mandatory.')])
    total_constructor_titles = IntegerField("Total constructor titles", [validators.NumberRange(min=0), validators.InputRequired('Input is mandatory.')])
    finishing_position_in_previous_season = IntegerField("Finishing position in previous season", [validators.NumberRange(min=0), validators.InputRequired('Input is mandatory.')])
    driver_belong_to_team = SelectField('Driver belongs to team', choices=[], validators=[validators.InputRequired('Team selection is mandatory.')])

    
    