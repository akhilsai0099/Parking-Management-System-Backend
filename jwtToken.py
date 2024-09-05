from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id: str = payload.get("username")
		if id is None:
			print("Invalid Id")
		token_data = {"id": id}
		return token_data
	except jwt.ExpiredSignatureError:
		print("Signature expired. Please log in again")
	except jwt.PyJWTError:
		print("Invalid token. Please log in again")
