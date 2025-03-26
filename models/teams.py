import uuid
from pydantic import BaseModel, PrivateAttr
from google.cloud.firestore_v1.base_query import FieldFilter

from f1_racer.firestore import initialize_firestore
from f1_racer.utils import cast_attribute_value

instance_db = initialize_firestore()

class Teams(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda:str(uuid.uuid4()))
    team_name: str
    year_founded: int
    total_pole_positions: int
    total_race_wins: int
    total_constructor_titles: int
    finishing_position_in_previous_season: int
    created_by: str
    
    def add_team(self):
        """
        Add this team's details to the Firestore 'teams' collection.
        Ensures that team names are unique.
        """
        try:
            # Check if a team with the same name already exists
            existing_teams = instance_db.collection("teams").where(
                filter=FieldFilter("team_name", "==", self.team_name)
            ).get()
            
            if len(existing_teams) > 0:
                return {"error": f"A team with the name '{self.team_name}' already exists."}
            
            team_data = self.model_dump()
            doc_ref = instance_db.collection("teams")
            doc_ref.document(self._id).set(team_data)
            return {"message": "Team added successfully", "team_id": self._id}
        except Exception as e:
            print(f"Error adding team: {e}")
            return {"error": str(e)}
    
    def edit_team(self, team_id: str):
        try:
            team_data = self.model_dump()
            doc_ref = instance_db.collection("teams").document(team_id)
            
            # Check if the document exists
            if not doc_ref.get().exists:
                return {"error": f"Team with ID {team_id} not found"}
            
            # Update the team document
            doc_ref.update(team_data)
            return {"message": f"Team with ID {team_id} updated successfully"}
        except Exception as e:
            print(f"Error editing team: {e}")
            return {"error": str(e)}

    @staticmethod
    def delete_team(team_id: str):
        try:
            doc_ref = instance_db.collection("teams").document(team_id)
            
            # Check if the document exists
            if not doc_ref.get().exists:
                return {"error": f"Team with ID {team_id} not found"}
            
            # Delete the team document
            doc_ref.delete()
            return {"message": f"Team with ID {team_id} deleted successfully"}
        except Exception as e:
            print(f"Error deleting team: {e}")
            return {"error": str(e)}  
    
    @staticmethod
    def get_team(team_id: str):
        """
        Fetch details of a team by ID from the Firestore 'teams' collection.
        """
        try:
            doc_ref = instance_db.collection("teams").document(team_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict() 
            else:
                print(f"Team with ID {team_id} not found")
                return {"error": f"Team with ID {team_id} not found"}
        except Exception as e:
            print(f"Error fetching team: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def get_teams_list(attribute=None, comparsion=None, attr_value=None):
        doc_ref = instance_db.collection("teams")
        if attribute and comparsion and attr_value:
            attr_value = cast_attribute_value(attribute, attr_value, Teams)
            doc_ref = doc_ref.where(filter=FieldFilter(attribute, comparsion, attr_value))
        doc_ref = (doc_ref.stream())
        docs = doc_ref
        teams = []
        for doc in docs:
            data = doc.to_dict()
            team_name = data.get("team_name", "Unknown")
            teams.append({"id": doc.id, "team_name": team_name})
            
        return teams
    
    @staticmethod
    def get_teams_comparison(team1, team2):
        doc_ref = instance_db.collection("teams").where(filter=FieldFilter("team_name", "in", [team1, team2]))
        doc_ref = (doc_ref.stream())
        docs = doc_ref
        teams = []
        for doc in docs:
            data = doc.to_dict()
            teams.append(data)
        return teams
        