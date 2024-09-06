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
    return f'Bearer {encoded_jwt}'

def verify_access_token(token: str):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		email: str = payload.get("email")
		if email is None:
			print("Invalid Id")
		token_data = {"email": email}
		return token_data
	except jwt.ExpiredSignatureError:
		print("Signature expired. Please log in again")
	except jwt.PyJWTError:
		print("Invalid token. Please log in again")
