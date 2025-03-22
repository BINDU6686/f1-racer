import requests

from google.cloud import firestore

config = {
    "apiKey": "AIzaSyDFyKJp_HDVwSAa5S72n3Xyk92UE04YhRs",
    "authDomain": "f1-racer-bef74.firebaseapp.com",
    "projectId": "f1-racer-bef74",
    "storageBucket": "f1-racer-bef74.firebasestorage.app",
    "messagingSenderId": "101888698498",
    "appId": "1:101888698498:web:e73c3bb678b112dada6c9b",
    "measurementId": "G-Y52LPS5CPT",
    "databaseURL": "https://f1-racer-bef74.firebaseio.com"
}

URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='

def sign_in_with_email_and_password(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(f"{URL}{config['apiKey']}", json=payload, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'No successfule login'}


async def authenticate(email_id: str, password: str) -> dict:
    """
    {'kind': '', 'localId': '', 'email': '', 'display
    Name': '', 'idToken': '', 'registered': True, 'refreshToken': '', 'expiresIn': '3600'}"""
    user = {}
    user = sign_in_with_email_and_password(email_id, password)
    
    return user




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