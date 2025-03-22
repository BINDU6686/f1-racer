from wtforms import Form, BooleanField, StringField, validators, IntegerField, FloatField

class TeamsForm(Form):
    year_founded = IntegerField('Year Founded', [
        validators.DataRequired(),
        validators.NumberRange(min=1950, max=2025, message="Year must be between 1950 and 2025")
    ])
    total_pole_position = IntegerField('Total Pole Positions', [
        validators.DataRequired(),
        validators.NumberRange(min=0, message="Value must be 0 or greater")
    ])
    total_race_wins = IntegerField('Total Race Wins', [
        validators.DataRequired(),
        validators.NumberRange(min=0, message="Value must be 0 or greater")
    ])
    total_constructor_titles = IntegerField('Total Constructor Titles', [
        validators.DataRequired(),
        validators.NumberRange(min=0, message="Value must be 0 or greater")
    ])
    finishing_position_in_previous_season = IntegerField('Previous Season Finishing Position', [
        validators.DataRequired(),
        validators.NumberRange(min=1, max=20, message="Position must be between 1 and 20")
    ])