from google.cloud import firestore


def initialize_firestore():
    """
    Initialize Firestore client using service account.
    """
    db = firestore.Client.from_service_account_json("./service-account-file.json")
    print("Firestore initialized successfully!")
    # users_ref = db.collection("drivers")
    # print(users_ref.document('G7XL0B3OHjCVvjMq9t2j').get().to_dict())
    # sf_landmarks = users_ref.document("SF").collection("landmarks")
    # sf_landmarks.document().set({"name": "Golden Gate Bridge", "type": "bridge"})


    return db

initialize_firestore()