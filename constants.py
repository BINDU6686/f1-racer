from enum import Enum

class Attribute(Enum):
    AGE = ("Age", "age")
    TOTAL_POLE_POSITION = ("Total Pole Positions", "total_pole_position")
    TOTAL_RACE_WINS = ("Total Race Wins", "total_race_wins")
    TOTAL_POINTS_SCORED = ("Total Points Scored", "total_points_scored")
    TOTAL_CONSTRUCTOR_TITLES = ("Constructor Titles", "total_constructor_titles")
    PREVIOUS_SEASON_POSITION = ("Previous Season Position", "finishing_position_in_previous_season")

    @property
    def visible_text(self):
        return self.value[0]

    @property
    def value_text(self):
        return self.value[1]
