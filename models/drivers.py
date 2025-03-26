import uuid
from pydantic import BaseModel, PrivateAttr
from google.cloud.firestore_v1.base_query import FieldFilter

from f1_racer.firestore import initialize_firestore
from f1_racer.utils import cast_attribute_value

instance_db = initialize_firestore()

class Drivers(BaseModel):
    _id: str = PrivateAttr(default_factory=lambda:str(uuid.uuid4()))
    driver_name: str
    age:int 
    total_pole_position:int
    total_race_wins: int
    total_points_scored:float
    total_constructor_titles:int
    finishing_position_in_previous_season: int
    created_by: str
    driver_belong_to_team: str
    
    
    def add_driver(self):

        try:
        # Check if a driver with the same name already exists
            existing_drivers = instance_db.collection("drivers").where(filter=FieldFilter("driver_name", "==", self.driver_name)).get()
      
            if len(existing_drivers) > 0:
                return {"error": f"A driver with the name '{self.driver_name}' already exists."}
            
            driver_data = self.model_dump()
            doc_ref = instance_db.collection("drivers")
            doc_ref.document(self._id).set(driver_data)
            return {"message": "Driver added successfully", "driver_id": self._id}
        except Exception as e:
            print(f"Error adding driver: {e}")
            return {"error": str(e)}
    
    
    def edit_driver(self, driver_id: str):
        try:
            driver_data = self.model_dump()
            doc_ref = instance_db.collection("drivers").document(driver_id)
            
            # Check if the document exists
            if not doc_ref.get().exists:
                return {"error": f"Driver with ID {driver_id} not found"}
            
            # Update the driver document
            doc_ref.update(driver_data)
            return {"message": f"Driver with ID {driver_id} updated successfully"}
        except Exception as e:
            print(f"Error editing driver: {e}")
            return {"error": str(e)}

    @staticmethod
    def delete_driver(driver_id: str):
        try:
            doc_ref = instance_db.collection("drivers").document(driver_id)
            
            # Check if the document exists
            if not doc_ref.get().exists:
                return {"error": f"Driver with ID {driver_id} not found"}
            
            # Delete the driver document
            doc_ref.delete()
            return {"message": f"Driver with ID {driver_id} deleted successfully"}
        except Exception as e:
            print(f"Error deleting driver: {e}")
            return {"error": str(e)}  
        
    
    @staticmethod
    def get_driver(driver_id: str):
        """
        Fetch details of a driver by ID from the Firestore 'drivers' collection.
        """
        try:
            doc_ref = instance_db.collection("drivers").document(driver_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict() 
            else:
                print(f"Driver with ID {driver_id} not found")
                return {"error": f"Driver with ID {driver_id} not found"}
        except Exception as e:
            print(f"Error fetching driver: {e}")
            return {"error": str(e)}
        
    @staticmethod
    def get_drivers_list(attribute=None, comparsion=None, attr_value=None):
            
        doc_ref = instance_db.collection("drivers")
        if attribute and comparsion and attr_value:
            attr_value = cast_attribute_value(attribute, attr_value, Drivers)
            doc_ref = doc_ref.where(filter=FieldFilter(attribute, comparsion, attr_value))
        doc_ref = (doc_ref.stream())
        docs = doc_ref
        drivers = []
        for doc in docs:
            data = doc.to_dict()
            driver_name = data.get("driver_name", "Unknown")
            drivers.append({"id": doc.id, "driver_name": driver_name})
            
        return drivers
    
    @staticmethod
    def get_drivers_comparison(driver1, driver2):
        doc_ref = instance_db.collection("drivers").where(filter=FieldFilter("driver_name", "in", [driver1, driver2]))
        doc_ref = (doc_ref.stream())
        docs = doc_ref
        drivers = []
        for doc in docs:
            data = doc.to_dict()
            drivers.append(data)
        return drivers
        
    

    
