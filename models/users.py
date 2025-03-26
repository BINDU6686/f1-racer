from pydantic import BaseModel, PrivateAttr
import uuid

import requests

from f1_racer.constants import FIREBASE_CONFIG, FIREBASE_URL

class Users(BaseModel):
    email: str 
    password: str
    
    def register_user(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True
        }
        response = requests.post(f"{FIREBASE_URL}accounts:signUp?key={FIREBASE_CONFIG['apiKey']}", json=payload, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Failed to register user', 'details': response.json()}

    async def sign_in_with_email_and_password(self):
        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True
        }
        response = requests.post(f"{FIREBASE_URL}accounts:signInWithPassword?key={FIREBASE_CONFIG['apiKey']}", json=payload, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'No successfule login'}

    
    async def authenticate(self) -> dict:
        """
        {'kind': '', 'localId': '', 'email': '', 'display
        Name': '', 'idToken': '', 'registered': True, 'refreshToken': '', 'expiresIn': '3600'}"""
        user = {}
        user = await self.sign_in_with_email_and_password()
        return user