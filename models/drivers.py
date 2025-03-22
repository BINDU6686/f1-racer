from pydantic import BaseModel, PrivateAttr
import uuid

from f1_racer.firestore import initialize_firestore

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
    
    
    def add_driver(self):
        """
        Add this driver's details to the Firestore 'drivers' collection.
        """
        try:
            driver_data = self.model_dump() 
            doc_ref = instance_db.collection("drivers")
            doc_ref.document(self._id).set(driver_data)  # Use `set` to save the data
            print(f"Driver added with ID: {self._id}")
            return {"message": "Driver added successfully", "driver_id": self._id}
        except Exception as e:
            print(f"Error adding driver: {e}")
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
                return doc.to_dict()  # Convert Firestore document to a dictionary
            else:
                print(f"Driver with ID {driver_id} not found")
                return {"error": f"Driver with ID {driver_id} not found"}
        except Exception as e:
            print(f"Error fetching driver: {e}")
            return {"error": str(e)}
        
    @staticmethod
    def get_drivers_list():
        doc_ref = instance_db.collection("drivers")
        docs = doc_ref.stream()
        drivers = []
        for doc in docs:
            data = doc.to_dict()
            driver_name = data.get("driver_name", "Unknown")
            drivers.append({"id": doc.id, "driver_name": driver_name})
            
        return drivers
        
    

    
