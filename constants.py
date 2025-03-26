from enum import Enum

class DriverAttribute(Enum):
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
    
class TeamAttribute(Enum):
    YEAR_FOUNDED = ("Year Founded", "year_founded")
    TOTAL_POLE_POSITIONS = ("Total Pole Positions", "total_pole_positions")
    TOTAL_RACE_WINS = ("Total Race Wins", "total_race_wins")
    TOTAL_CONSTRUCTOR_TITLES = ("Constructor Titles", "total_constructor_titles")
    PREVIOUS_SEASON_POSITION = ("Previous Season Position", "finishing_position_in_previous_season")

    @property
    def visible_text(self):
        return self.value[0]

    @property
    def value_text(self):
        return self.value[1]


class Operator(Enum):
    EQUALS = ("Equals", "==")
    GREATER_THAN = ("Greater Than", ">")
    LESS_THAN = ("Less Than", "<")
    GREATER_THAN_OR_EQUAL = ("Greater Than or Equal", ">=")
    LESS_THAN_OR_EQUAL = ("Less Than or Equal", "<=")
    NOT_EQUAL = ("Not Equal", "!=")

    @property
    def visible_text(self):
        return self.value[0]

    @property
    def operator_symbol(self):
        return self.value[1]




FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDFyKJp_HDVwSAa5S72n3Xyk92UE04YhRs",
    "authDomain": "f1-racer-bef74.firebaseapp.com",
    "projectId": "f1-racer-bef74",
    "storageBucket": "f1-racer-bef74.firebasestorage.app",
    "messagingSenderId": "101888698498",
    "appId": "1:101888698498:web:e73c3bb678b112dada6c9b",
    "measurementId": "G-Y52LPS5CPT",
    "databaseURL": "https://f1-racer-bef74.firebaseio.com"
}

FIREBASE_URL = 'https://identitytoolkit.googleapis.com/v1/'


